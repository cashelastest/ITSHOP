from rest_framework import permissions

class IsSellerOrReadOnly(permissions.BasePermission):
	def has_object_permission(self, request, view, obj):
		if request.method in permissions.SAFE_METHODS:
			return True
		print(request.user)
		print(obj.seller.user)
		print(bool(obj.seller.user == request.user))
		return bool(obj.seller.user == request.user)