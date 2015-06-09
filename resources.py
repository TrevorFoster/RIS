import pygame, os

class ResourceManager:
	resources = {}

	@staticmethod
	def loadImage(path):
		resources = ResourceManager.resources

		if path in resources:
			return resources[path]
		elif not os.path.isfile(path):
			return None
		else:
			img = pygame.image.load(path).convert_alpha()
			assert img, "Image could not be loaded."

			resources[path] = img
			return img


	@staticmethod
	def get(path):
		return ResourceManager.resources.get(path)

