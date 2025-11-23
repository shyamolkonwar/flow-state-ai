"""
Reusable UI Components for FlowFacilitator
Premium, animated components with glassmorphism effects
"""

from PyQt6.QtWidgets import (
    QPushButton, QLabel, QFrame, QVBoxLayout, QHBoxLayout,
    QWidget, QGraphicsOpacityEffect
)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QSize, pyqtProperty
from PyQt6.QtGui import QPixmap, QPainter, QPainterPath, QColor, QFont

from .styles import (
    get_button_style, get_card_style, get_label_style,
    COLORS, STATUS_COLORS
)


class PremiumButton(QPushButton):
    """Animated button with glow effect"""
    
    def __init__(self, text: str, variant: str = 'primary', parent=None):
        super().__init__(text, parent)
        self.variant = variant
        self.setStyleSheet(get_button_style(variant))
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Add opacity effect for animations
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.opacity_effect.setOpacity(1.0)
        
        # Animation for hover
        self.hover_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.hover_animation.setDuration(200)
        self.hover_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
    
    def enterEvent(self, event):
        """Animate on hover"""
        self.hover_animation.stop()
        self.hover_animation.setStartValue(1.0)
        self.hover_animation.setEndValue(0.9)
        self.hover_animation.start()
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        """Animate on leave"""
        self.hover_animation.stop()
        self.hover_animation.setStartValue(0.9)
        self.hover_animation.setEndValue(1.0)
        self.hover_animation.start()
        super().leaveEvent(event)


class StatusIndicator(QWidget):
    """Colored dot with label for status display"""
    
    def __init__(self, status: str, label: str, parent=None):
        super().__init__(parent)
        self.status = status
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        
        # Status dot
        self.dot = QLabel()
        self.dot.setFixedSize(12, 12)
        self.update_status(status)
        
        # Label
        label_widget = QLabel(label)
        label_widget.setStyleSheet(get_label_style('body'))
        
        layout.addWidget(self.dot)
        layout.addWidget(label_widget)
        layout.addStretch()
    
    def update_status(self, status: str):
        """Update the status color"""
        self.status = status
        color = STATUS_COLORS.get(status, STATUS_COLORS['idle'])
        self.dot.setStyleSheet(f"""
            QLabel {{
                background-color: {color};
                border-radius: 6px;
            }}
        """)


class PermissionCard(QFrame):
    """Card showing permission status with grant button"""
    
    def __init__(self, name: str, granted: bool, optional: bool = False, parent=None):
        super().__init__(parent)
        self.name = name
        self.granted = granted
        self.optional = optional
        
        self.setStyleSheet(get_card_style())
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        
        # Icon and name
        info_layout = QVBoxLayout()
        
        name_label = QLabel(name)
        name_label.setStyleSheet(get_label_style('body'))
        
        if optional:
            optional_label = QLabel("(Optional)")
            optional_label.setStyleSheet(get_label_style('secondary'))
            info_layout.addWidget(name_label)
            info_layout.addWidget(optional_label)
        else:
            info_layout.addWidget(name_label)
        
        layout.addLayout(info_layout)
        layout.addStretch()
        
        # Status indicator
        if granted:
            status_label = QLabel("✓")
            status_label.setStyleSheet(f"""
                QLabel {{
                    color: {COLORS['teal']};
                    font-size: 24px;
                    font-weight: bold;
                }}
            """)
            layout.addWidget(status_label)
        else:
            warning_label = QLabel("⚠")
            warning_label.setStyleSheet(f"""
                QLabel {{
                    color: {COLORS['gold']};
                    font-size: 24px;
                }}
            """)
            layout.addWidget(warning_label)
            
            # Grant button
            self.grant_button = PremiumButton("Grant", variant='primary')
            layout.addWidget(self.grant_button)


class SectionHeader(QLabel):
    """Styled section header"""
    
    def __init__(self, text: str, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet(get_label_style('section'))


class InfoCard(QFrame):
    """Glassmorphism card container"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(get_card_style())
        
        # Add subtle shadow effect
        self.setGraphicsEffect(None)  # Can add QGraphicsDropShadowEffect if needed


class RoundLogo(QLabel):
    """Logo component that makes square images round"""
    
    def __init__(self, image_path: str, size: int = 80, parent=None):
        super().__init__(parent)
        self.image_path = image_path
        self.logo_size = size
        
        self.setFixedSize(size, size)
        self.load_image()
    
    def load_image(self):
        """Load and display the image as a circle"""
        pixmap = QPixmap(self.image_path)
        
        if pixmap.isNull():
            # Fallback to a colored circle if image not found
            self.create_fallback_logo()
            return
        
        # Scale pixmap to size
        pixmap = pixmap.scaled(
            self.logo_size, self.logo_size,
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )
        
        # Create circular mask
        rounded = QPixmap(self.logo_size, self.logo_size)
        rounded.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(rounded)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Create circular path
        path = QPainterPath()
        path.addEllipse(0, 0, self.logo_size, self.logo_size)
        
        painter.setClipPath(path)
        
        # Center the image
        x = (self.logo_size - pixmap.width()) // 2
        y = (self.logo_size - pixmap.height()) // 2
        painter.drawPixmap(x, y, pixmap)
        
        painter.end()
        
        self.setPixmap(rounded)
    
    def create_fallback_logo(self):
        """Create a fallback colored circle"""
        pixmap = QPixmap(self.logo_size, self.logo_size)
        pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw gradient circle
        painter.setBrush(QColor(COLORS['teal']))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(0, 0, self.logo_size, self.logo_size)
        
        # Draw "FF" text
        painter.setPen(QColor(COLORS['deep_night']))
        font = QFont('SF Pro Display', self.logo_size // 3, QFont.Weight.Bold)
        painter.setFont(font)
        painter.drawText(0, 0, self.logo_size, self.logo_size, 
                        Qt.AlignmentFlag.AlignCenter, "FF")
        
        painter.end()
        
        self.setPixmap(pixmap)


class AnimatedWidget(QWidget):
    """Base widget with fade in/out animations"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Opacity effect for fade animations
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(0.0)
        
        # Fade animation
        self.fade_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_animation.setDuration(300)
        self.fade_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
    
    def fade_in(self):
        """Fade in animation"""
        self.fade_animation.stop()
        self.fade_animation.setStartValue(0.0)
        self.fade_animation.setEndValue(1.0)
        self.fade_animation.start()
    
    def fade_out(self):
        """Fade out animation"""
        self.fade_animation.stop()
        self.fade_animation.setStartValue(1.0)
        self.fade_animation.setEndValue(0.0)
        self.fade_animation.start()


class GradientLabel(QLabel):
    """Label with gradient text effect"""
    
    def __init__(self, text: str, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet(f"""
            QLabel {{
                color: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 {COLORS['teal']},
                    stop:1 {COLORS['cyan']}
                );
                font-size: 28px;
                font-weight: 700;
            }}
        """)
