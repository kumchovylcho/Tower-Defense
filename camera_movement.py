import pygame as pg


class CameraMovement:
    def __init__(self,
                 camera_x: int,
                 camera_y: int,
                 zoom_level: float,
                 min_zoom: float,
                 max_zoom: float,
                 zoom_speed: float,
                 zoom_step_speed: float,
                 drag_friction: float,
                 drag_momentum_threshold: float
                 ):
        self.camera_x = camera_x
        self.camera_y = camera_y
        self.zoom_level = zoom_level
        self.target_zoom_level = zoom_level
        self.min_zoom = min_zoom
        self.max_zoom = max_zoom
        self.zoom_speed = zoom_speed
        # this is for smooth zooming and zooming out
        self.zoom_step_speed = zoom_step_speed
        self.is_being_dragged = False
        self.last_mouse_pos = None

        # drag momentum settings
        self.velocity_x = 0
        self.velocity_y = 0
        # friction to reduce momentum over time
        self.drag_friction = drag_friction
        # threshold to stop momentum completely
        self.momentum_threshold = drag_momentum_threshold

    def adjust_zoom_level(self, event_y: int):
        # update the target zoom level based on the scroll input
        self.target_zoom_level += event_y * self.zoom_speed
        self.target_zoom_level = max(self.min_zoom, min(self.max_zoom, self.target_zoom_level))

    def smooth_zoom(self):
        if abs(self.zoom_level - self.target_zoom_level) > self.zoom_step_speed:
            if self.zoom_level < self.target_zoom_level:
                self.zoom_level += self.zoom_step_speed
            elif self.zoom_level >= self.target_zoom_level:
                self.zoom_level -= self.zoom_step_speed
        else:
            self.zoom_level = self.target_zoom_level

    def smooth_drag_on_release(self):
        self.camera_x += self.velocity_x
        self.camera_y += self.velocity_y

        # reduce velocity using friction
        self.velocity_x *= self.drag_friction
        self.velocity_y *= self.drag_friction

        # stop movement if velocity is below the threshold
        if abs(self.velocity_x) < self.momentum_threshold:
            self.velocity_x = 0
        if abs(self.velocity_y) < self.momentum_threshold:
            self.velocity_y = 0

    def activate_dragging_camera(self, is_button_pressed: bool, is_button_released: bool):
        if is_button_pressed:
            self.is_being_dragged = True
            self.last_mouse_pos = pg.mouse.get_pos()
            self.velocity_x = 0
            self.velocity_y = 0
        elif is_button_released:
            self.is_being_dragged = False
            self.last_mouse_pos = None

    def drag_the_camera(self):
        current_mouse_pos = pg.mouse.get_pos()
        if self.last_mouse_pos:
            # calculate the delta movement of the mouse
            delta_x = current_mouse_pos[0] - self.last_mouse_pos[0]
            delta_y = current_mouse_pos[1] - self.last_mouse_pos[1]

            # update camera position
            self.camera_x += delta_x
            self.camera_y += delta_y

            # update velocity for momentum
            self.velocity_x = delta_x
            self.velocity_y = delta_y

        # update last mouse position
        self.last_mouse_pos = current_mouse_pos

    def move_camera(self):
        if not self.is_being_dragged:
            self.smooth_drag_on_release()
        elif self.is_being_dragged:
            self.drag_the_camera()

        self.smooth_zoom()