import glfw
from camera import Camera

class Movement:

	def __init__(self, width, height):
		self.boosted_speed = 0.25
		self.normal_speed = 0.01
		self.camera = Camera()

		self.left = False
		self.right = False
		self.forward = False
		self.backward = False
		self.boost = False

		self.first_mouse = True
		self.lastX = width / 2
		self.lastY = height / 2


	def keyboard_callback(self, window, key, scancode, action, mode):
		if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
			glfw.set_window_should_close(window, True)
		if key == glfw.KEY_W and action == glfw.PRESS:
			self.forward = True
		elif key == glfw.KEY_W and action == glfw.RELEASE:
			self.forward = False
		if key == glfw.KEY_S and action == glfw.PRESS:
			self.backward = True
		elif key == glfw.KEY_S and action == glfw.RELEASE:
			self.backward = False
		if key == glfw.KEY_A and action == glfw.PRESS:
			self.left = True
		elif key == glfw.KEY_A and action == glfw.RELEASE:
			self.left = False
		if key == glfw.KEY_D and action == glfw.PRESS:
			self.right = True
		elif key == glfw.KEY_D and action == glfw.RELEASE:
			self.right = False
		if key == glfw.KEY_LEFT_SHIFT and action == glfw.PRESS:
			self.boost = True
		elif key == glfw.KEY_LEFT_SHIFT and action == glfw.RELEASE:
			self.boost = False
		

	def mouse_callback(self, window, xpos, ypos):
		if self.first_mouse:
			self.lastX = xpos
			self.lastY = ypos
			self.first_mouse = False

		xoffset = xpos - self.lastX
		yoffset = self.lastY - ypos

		self.lastX = xpos
		self.lastY = ypos

		self.camera.process_mouse_movement(xoffset, yoffset)


	def do(self):
		speed = self.boosted_speed if self.boost else self.normal_speed

		if self.left:
			self.camera.process_keyboard("LEFT", speed)
		if self.right:
			self.camera.process_keyboard("RIGHT", speed)
		if self.forward:
			self.camera.process_keyboard("FORWARD", speed)
		if self.backward:
			self.camera.process_keyboard("BACKWARD", speed)


	def get_view(self):
		return self.camera.get_view_matrix()

