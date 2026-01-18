"""
Interfaz del Repositorio de Carrito

Puerto (Port) en la arquitectura hexagonal.
Define el contrato que deben implementar los adaptadores de persistencia.

Implementaciones:
- PostgreSqlCarritoRepository (producción)
- InMemoryCarritoRepository (testing/desarrollo)
"""
from abc import abstractmethod
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from .base import RepositorioBase
from ..entities.carrito import Carrito
from shared.enums.estado_carrito import EstadoCarrito


class CarritoRepository(RepositorioBase[Carrito]):
    """
    Repositorio de Carrito de Compras.
    
    Responsabilidades:
    - Persistir y recuperar carritos
    - Gestionar unicidad de carrito activo por usuario
    - Control de concurrencia con versión
    - Gestión de expiración
    
    Invariantes:
    - Solo un carrito ACTIVO por usuario
    - Usar version para optimistic locking
    - Respetar policy switch de persistencia
    """
    
    @abstractmethod
    def obtener_por_id(self, id: UUID) -> Optional[Carrito]:
        """
        Obtiene un carrito por su ID.
        
        Args:
            id: UUID del carrito
            
        Returns:
            Carrito si existe, None si no
        """
        pass
    
    @abstractmethod
    def obtener_carrito_activo_usuario(self, usuario_id: UUID) -> Optional[Carrito]:
        """
        Obtiene el carrito activo de un usuario.
        
        REGLA: Solo puede haber un carrito activo por usuario.
        Estados activos: CREADO, ACTIVO, BLOQUEADO
        
        Args:
            usuario_id: UUID del usuario
            
        Returns:
            Carrito activo si existe, None si no
        """
        pass
    
    @abstractmethod
    def guardar(self, carrito: Carrito) -> Carrito:
        """
        Guarda un carrito (crear o actualizar).
        
        IMPORTANTE: Debe validar versión para optimistic locking.
        Si la versión en BD no coincide, lanzar excepción de concurrencia.
        
        Args:
            carrito: Carrito a guardar
            
        Returns:
            Carrito guardado con versión actualizada
            
        Raises:
            ConcurrencyError: Si hay conflicto de versión
        """
        pass
    
    @abstractmethod
    def eliminar(self, id: UUID) -> bool:
        """
        Elimina un carrito (hard delete).
        
        Usar con precaución. Preferir expirar() para mantener historial.
        
        Args:
            id: UUID del carrito
            
        Returns:
            True si se eliminó, False si no existía
        """
        pass
    
    @abstractmethod
    def obtener_carritos_expirados(self, fecha_limite: datetime) -> List[Carrito]:
        """
        Obtiene carritos que han expirado.
        
        Usado por job de limpieza/expiración.
        
        Args:
            fecha_limite: Fecha límite de expiración
            
        Returns:
            Lista de carritos expirados (no en estado EXPIRADO aún)
        """
        pass
    
    @abstractmethod
    def obtener_carritos_por_estado(self, estado: EstadoCarrito) -> List[Carrito]:
        """
        Obtiene todos los carritos en un estado específico.
        
        Args:
            estado: Estado a filtrar
            
        Returns:
            Lista de carritos en ese estado
        """
        pass
    
    @abstractmethod
    def obtener_historial_usuario(
        self, 
        usuario_id: UUID, 
        incluir_expirados: bool = False
    ) -> List[Carrito]:
        """
        Obtiene el historial de carritos de un usuario.
        
        Args:
            usuario_id: UUID del usuario
            incluir_expirados: Si incluir carritos expirados
            
        Returns:
            Lista de carritos del usuario
        """
        pass
    
    @abstractmethod
    def existe(self, id: UUID) -> bool:
        """
        Verifica si existe un carrito con el ID dado.
        
        Args:
            id: UUID del carrito
            
        Returns:
            True si existe, False si no
        """
        pass
    
    @abstractmethod
    def contar_por_estado(self, estado: EstadoCarrito) -> int:
        """
        Cuenta carritos por estado.
        
        Útil para métricas y dashboards.
        
        Args:
            estado: Estado a contar
            
        Returns:
            Cantidad de carritos en ese estado
        """
        pass
    
    @abstractmethod
    def bloquear_para_checkout(self, id: UUID, version: int) -> bool:
        """
        Bloquea un carrito para checkout con control de concurrencia.
        
        Operación atómica que:
        1. Verifica que la versión coincida
        2. Cambia estado a BLOQUEADO
        3. Incrementa versión
        
        Args:
            id: UUID del carrito
            version: Versión esperada (optimistic locking)
            
        Returns:
            True si se bloqueó exitosamente
            
        Raises:
            ConcurrencyError: Si hay conflicto de versión
            ReglaNegocioViolada: Si el carrito no puede bloquearse
        """
        pass
