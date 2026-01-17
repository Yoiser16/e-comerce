"""
URL Configuration para Django
"""
from django.contrib import admin
from django.urls import path, include

# Importar views de autenticación
from interfaces.api.rest.views.auth_views import (
    LoginView,
    LogoutView,
    RefreshTokenView,
    VerifyTokenView,
    PerfilUsuarioView,
)

# Importar health checks
from interfaces.api.rest.views.health_view import (
    HealthCheckView,
    ReadinessCheckView,
    LivenessCheckView,
)

urlpatterns = [
    # Health Checks (públicos, sin autenticación)
    path('health', HealthCheckView.as_view(), name='health-check'),
    path('ready', ReadinessCheckView.as_view(), name='readiness-check'),
    path('live', LivenessCheckView.as_view(), name='liveness-check'),
    
    path('admin/', admin.site.urls),
    
    # Autenticación JWT
    path('api/v1/auth/login', LoginView.as_view(), name='auth-login'),
    path('api/v1/auth/logout', LogoutView.as_view(), name='auth-logout'),
    path('api/v1/auth/refresh', RefreshTokenView.as_view(), name='auth-refresh'),
    path('api/v1/auth/verify', VerifyTokenView.as_view(), name='auth-verify'),
    path('api/v1/auth/perfil', PerfilUsuarioView.as_view(), name='auth-perfil'),
    
    # API REST (protegida con JWT)
    path('api/v1/', include('interfaces.api.rest.urls')),
]
