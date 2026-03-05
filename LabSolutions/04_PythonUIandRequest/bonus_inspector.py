"""
Bonus module to inspect and visualize multiple .laz files stitched in 2D.
Features header-parsing, true geographical aspect ratios,
filename tracking, RGB toggle, and Contour toggles.
"""
import numpy as np
import laspy
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QProgressBar, QCheckBox, QGraphicsView,
                               QGraphicsScene, QGraphicsPixmapItem)
from PySide6.QtGui import QImage, QPixmap, QPainter, QPen, QColor
from PySide6.QtCore import Qt, QThread, Signal

class InteractiveGraphicsView(QGraphicsView):
    """A QGraphicsView that handles zooming, panning, and precise coordinate mapping."""
    def __init__(self, parent=None):
        super().__init__(parent)

        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        # Base image layer
        self.pixmap_item = QGraphicsPixmapItem()
        self.pixmap_item.setZValue(0)
        self.scene.addItem(self.pixmap_item)

        # Transparent overlay layer for contours
        self.contour_item = QGraphicsPixmapItem()
        self.contour_item.setZValue(1) # Sits on top of the base image
        self.scene.addItem(self.contour_item)

        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setMouseTracking(True)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)

        self.grid_z = None
        self.source_grid = None
        self.file_names = []
        self.geo_info = {}
        self.info_label = None

    def set_pixmap(self, pixmap):
        self.pixmap_item.setPixmap(pixmap)
        self.scene.setSceneRect(self.pixmap_item.boundingRect())

    def wheelEvent(self, event):
        zoom_in_factor = 1.15
        zoom_out_factor = 1.0 / zoom_in_factor
        if event.angleDelta().y() > 0:
            self.scale(zoom_in_factor, zoom_in_factor)
        else:
            self.scale(zoom_out_factor, zoom_out_factor)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)

        if self.grid_z is None or self.info_label is None:
            return

        scene_pos = self.mapToScene(event.position().toPoint())
        px, py = scene_pos.x(), scene_pos.y()

        h, w = self.grid_z.shape
        if 0 <= px < w and 0 <= py < h:
            py_int, px_int = int(py), int(px)
            z_val = self.grid_z[py_int, px_int]

            x_range = self.geo_info['x_max'] - self.geo_info['x_min']
            y_range = self.geo_info['y_max'] - self.geo_info['y_min']

            real_x = self.geo_info['x_min'] + (px / w) * x_range
            real_y = self.geo_info['y_max'] - (py / h) * y_range

            source_idx = self.source_grid[py_int, px_int]
            source_str = self.file_names[source_idx] if source_idx != -1 else "None (Empty Space)"
            z_str = "No Data" if np.isnan(z_val) else f"{z_val:.2f} m"

            msg = (f"<b>X:</b> {real_x:.2f} | <b>Y:</b> {real_y:.2f} | "
                   f"<b>Elevation:</b> {z_str} | "
                   f"<b>File:</b> {source_str}")

            self.info_label.setText(msg)


class RenderWorker(QThread):
    finished = Signal(np.ndarray, object, np.ndarray, np.ndarray, np.ndarray, list, dict, list, list)
    error = Signal(str)

    def __init__(self, file_paths: list):
        super().__init__()
        self.file_paths = file_paths

    def run(self):
        try:
            MAX_IMG_SIZE = 1000
            file_names = []
            available_dims = set()
            has_color_overall = False
            tile_rects = []

            global_x_min, global_x_max = float('inf'), float('-inf')
            global_y_min, global_y_max = float('inf'), float('-inf')

            for path in self.file_paths:
                file_names.append(path.split("/")[-1])
                with laspy.open(path) as f:
                    header = f.header
                    dims = list(header.point_format.dimension_names)
                    available_dims.update(dims)
                    if all(c in dims for c in ('red', 'green', 'blue')):
                        has_color_overall = True

                    local_min_x, local_max_x = header.x_min, header.x_max
                    local_min_y, local_max_y = header.y_min, header.y_max
                    global_x_min = min(global_x_min, local_min_x)
                    global_x_max = max(global_x_max, local_max_x)
                    global_y_min = min(global_y_min, local_min_y)
                    global_y_max = max(global_y_max, local_max_y)
                    tile_rects.append((local_min_x, local_max_x, local_min_y, local_max_y))

            x_range = global_x_max - global_x_min
            y_range = global_y_max - global_y_min

            if x_range > y_range:
                IMG_WIDTH = MAX_IMG_SIZE
                IMG_HEIGHT = int(MAX_IMG_SIZE * (y_range / x_range))
            else:
                IMG_HEIGHT = MAX_IMG_SIZE
                IMG_WIDTH = int(MAX_IMG_SIZE * (x_range / y_range))

            IMG_WIDTH = max(1, IMG_WIDTH)
            IMG_HEIGHT = max(1, IMG_HEIGHT)

            geo_info = {
                'x_min': global_x_min, 'x_max': global_x_max,
                'y_min': global_y_min, 'y_max': global_y_max
            }

            z_grid = np.full((IMG_HEIGHT, IMG_WIDTH), np.nan)
            source_grid = np.full((IMG_HEIGHT, IMG_WIDTH), -1, dtype=np.int16)
            rgb_grid = np.zeros((IMG_HEIGHT, IMG_WIDTH, 3), dtype=np.uint8) if has_color_overall else None

            pixel_tile_rects = []
            for (min_x, max_x, min_y, max_y) in tile_rects:
                px_min_x = int(((min_x - global_x_min) / x_range) * (IMG_WIDTH - 1))
                px_max_x = int(((max_x - global_x_min) / x_range) * (IMG_WIDTH - 1))
                px_max_y = int(((global_y_max - min_y) / y_range) * (IMG_HEIGHT - 1))
                px_min_y = int(((global_y_max - max_y) / y_range) * (IMG_HEIGHT - 1))
                pixel_tile_rects.append((px_min_x, px_min_y, px_max_x - px_min_x, px_max_y - px_min_y))

            for i, path in enumerate(self.file_paths):
                las = laspy.read(path)
                col_indices = ((las.x - global_x_min) / x_range * (IMG_WIDTH - 1)).astype(int)
                row_indices = ((global_y_max - las.y) / y_range * (IMG_HEIGHT - 1)).astype(int)
                sort_idx = np.argsort(las.z)

                z_grid[row_indices[sort_idx], col_indices[sort_idx]] = las.z[sort_idx]
                source_grid[row_indices[sort_idx], col_indices[sort_idx]] = i

                if has_color_overall and all(c in las.point_format.dimension_names for c in ('red', 'green', 'blue')):
                    rgb_grid[row_indices[sort_idx], col_indices[sort_idx], 0] = np.right_shift(las.red[sort_idx], 8).astype(np.uint8)
                    rgb_grid[row_indices[sort_idx], col_indices[sort_idx], 1] = np.right_shift(las.green[sort_idx], 8).astype(np.uint8)
                    rgb_grid[row_indices[sort_idx], col_indices[sort_idx], 2] = np.right_shift(las.blue[sort_idx], 8).astype(np.uint8)

            z_min, z_max = np.nanmin(z_grid), np.nanmax(z_grid)
            z_grid_filled = np.nan_to_num(z_grid, nan=z_min)

            # Base Heightmap
            z_norm = ((z_grid_filled - z_min) / (z_max - z_min) * 255).astype(np.uint8)
            z_norm[np.isnan(z_grid)] = 0

            # Transparent Contour Overlay (Slightly Blue)
            contour_interval = 20
            contour_mask = (z_grid_filled % contour_interval) < (contour_interval * 0.1)
            contour_mask[np.isnan(z_grid)] = False

            contours_rgba = np.zeros((IMG_HEIGHT, IMG_WIDTH, 4), dtype=np.uint8)
            contours_rgba[contour_mask] = [80, 150, 255, 200]

            z_norm = np.ascontiguousarray(z_norm)
            contours_rgba = np.ascontiguousarray(contours_rgba)
            if rgb_grid is not None:
                rgb_grid = np.ascontiguousarray(rgb_grid)

            friendly_dims = sorted(list(available_dims))
            self.finished.emit(z_norm, rgb_grid, contours_rgba, z_grid, source_grid, file_names, geo_info, friendly_dims, pixel_tile_rects)

        except Exception as e:
            self.error.emit(str(e))


class LidarInspector(QWidget):
    def __init__(self, file_paths: list):
        super().__init__()

        self.setWindowTitle(f"LiDAR Stitched Preview - {len(file_paths)} files")
        self.resize(1000, 800)

        self.layout = QVBoxLayout(self)

        # --- Top Header Area ---
        self.header_layout = QHBoxLayout()

        self.legend_box = QLabel("Loading data fields...")
        self.legend_box.setWordWrap(True)
        self.legend_box.setStyleSheet("background-color: #2b2b2b; color: white; padding: 10px; border-radius: 5px;")

        self.chk_color = QCheckBox("Show RGB Color")
        self.chk_color.setStyleSheet("font-weight: bold; font-size: 14px;")
        self.chk_color.hide()
        self.chk_color.toggled.connect(self.toggle_view_mode)

        self.chk_contours = QCheckBox("Show Contours")
        self.chk_contours.setStyleSheet("font-weight: bold; font-size: 14px;")
        self.chk_contours.setChecked(True)
        self.chk_contours.hide()
        self.chk_contours.toggled.connect(self.toggle_contours)

        self.header_layout.addWidget(self.legend_box)
        self.header_layout.addWidget(self.chk_color)
        self.header_layout.addWidget(self.chk_contours)

        self.info_label = QLabel("Loading and projecting LiDAR data (True Scale)...")
        self.info_label.setStyleSheet("font-size: 14px; padding: 5px; font-weight: bold;")

        self.loading_bar = QProgressBar()
        self.loading_bar.setRange(0, 0)

        self.image_view = InteractiveGraphicsView()
        self.image_view.info_label = self.info_label

        self.layout.addLayout(self.header_layout)
        self.layout.addWidget(self.info_label)
        self.layout.addWidget(self.loading_bar)
        self.layout.addWidget(self.image_view)

        self.height_pixmap = None
        self.color_pixmap = None

        self.render_worker = RenderWorker(file_paths)
        self.render_worker.finished.connect(self.on_render_finished)
        self.render_worker.error.connect(self.on_render_error)
        self.render_worker.start()

    def draw_tile_borders(self, qimage, tile_rects):
        painter = QPainter(qimage)
        pen = QPen(QColor(0, 255, 255, 120))
        pen.setStyle(Qt.DashLine)
        pen.setWidth(2)
        painter.setPen(pen)
        for rect in tile_rects:
            painter.drawRect(*rect)
        painter.end()
        return QPixmap.fromImage(qimage)

    def on_render_finished(self, z_norm, rgb_grid, contours_rgba, z_grid, source_grid, file_names, geo_info, available_dims, tile_rects):
        self.loading_bar.hide()
        self.info_label.setText("Hover over the image to see elevation and filename...")
        self.info_label.setStyleSheet("font-size: 14px; padding: 5px; font-weight: normal;")

        dims_str = ", ".join(available_dims)
        self.legend_box.setText(f"<b style='font-size: 14px;'>Contained Data Fields:</b><br/>{dims_str}")

        self._z_norm_cache = z_norm
        self._rgb_cache = rgb_grid
        self._contours_cache = contours_rgba

        h, w = self._z_norm_cache.shape

        # Build Base Heightmap
        height_img = QImage(self._z_norm_cache.data, w, h, w, QImage.Format_Grayscale8)
        self.height_pixmap = self.draw_tile_borders(height_img, tile_rects)

        # Build Contours Overlay
        contour_img = QImage(self._contours_cache.data, w, h, w * 4, QImage.Format_RGBA8888)
        self.image_view.contour_item.setPixmap(QPixmap.fromImage(contour_img))
        self.chk_contours.show()

        # Build RGB Base Map
        if self._rgb_cache is not None:
            color_img = QImage(self._rgb_cache.data, w, h, w * 3, QImage.Format_RGB888)
            self.color_pixmap = self.draw_tile_borders(color_img, tile_rects)
            self.chk_color.show()

        self.image_view.grid_z = z_grid
        self.image_view.source_grid = source_grid
        self.image_view.file_names = file_names
        self.image_view.geo_info = geo_info

        self.toggle_view_mode()

    def toggle_view_mode(self):
        if self.chk_color.isChecked() and self.color_pixmap:
            self.image_view.set_pixmap(self.color_pixmap)
        else:
            if self.height_pixmap:
                self.image_view.set_pixmap(self.height_pixmap)

    def toggle_contours(self):
        self.image_view.contour_item.setVisible(self.chk_contours.isChecked())

    def on_render_error(self, err_msg):
        self.loading_bar.hide()
        self.info_label.setText(f"<span style='color:red;'>Error merging LAZ: {err_msg}</span>")