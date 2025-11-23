"""
Premium UI Styles for FlowFacilitator
Centralized stylesheet definitions using the specified color palette
"""

# Color Palette
COLORS = {
    # Primary colors
    'crystal_white': '#FFFFFF',
    'deep_night': '#0B0710',
    
    # Accent colors
    'teal': '#2FE6C1',
    'cyan': '#4DE5FF',
    'magenta': '#FF6EC7',
    'gold': '#FFC66B',
    
    # Neutral palette
    'text_on_dark': '#EDEFF6',
    'text_secondary': '#B7BAC5',
    'surface_light': '#0F1220',
    'surface_elev': '#141722',
}

# Status colors
STATUS_COLORS = {
    'idle': '#6B7280',      # Gray
    'tracking': '#4DE5FF',  # Cyan
    'flow': '#2FE6C1',      # Teal
    'error': '#FF6EC7',     # Magenta
}


def get_window_style():
    """Main window stylesheet with glassmorphism effect"""
    return f"""
        QWidget {{
            background-color: {COLORS['deep_night']};
            color: {COLORS['text_on_dark']};
            font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', sans-serif;
        }}
        
        QMainWindow {{
            background-color: {COLORS['deep_night']};
            border-radius: 12px;
        }}
    """


def get_button_style(variant='primary'):
    """Premium button styles with hover animations"""
    if variant == 'primary':
        bg_color = COLORS['teal']
        hover_color = COLORS['cyan']
        text_color = COLORS['deep_night']
    elif variant == 'secondary':
        bg_color = COLORS['surface_elev']
        hover_color = COLORS['surface_light']
        text_color = COLORS['text_on_dark']
    elif variant == 'accent':
        bg_color = COLORS['magenta']
        hover_color = COLORS['gold']
        text_color = COLORS['crystal_white']
    else:
        bg_color = COLORS['surface_light']
        hover_color = COLORS['surface_elev']
        text_color = COLORS['text_on_dark']
    
    return f"""
        QPushButton {{
            background-color: {bg_color};
            color: {text_color};
            border: none;
            border-radius: 8px;
            padding: 12px 24px;
            font-size: 14px;
            font-weight: 600;
            min-width: 100px;
        }}
        
        QPushButton:hover {{
            background-color: {hover_color};
        }}
        
        QPushButton:pressed {{
            background-color: {bg_color};
            padding: 13px 24px 11px 24px;
        }}
        
        QPushButton:disabled {{
            background-color: {COLORS['surface_light']};
            color: {COLORS['text_secondary']};
        }}
    """


def get_card_style():
    """Glassmorphism card style"""
    return f"""
        QFrame {{
            background-color: {COLORS['surface_light']};
            border: 1px solid {COLORS['surface_elev']};
            border-radius: 12px;
            padding: 16px;
        }}
    """


def get_label_style(variant='body'):
    """Text label styles"""
    if variant == 'heading':
        return f"""
            QLabel {{
                color: {COLORS['text_on_dark']};
                font-size: 24px;
                font-weight: 700;
                padding: 8px 0;
            }}
        """
    elif variant == 'subheading':
        return f"""
            QLabel {{
                color: {COLORS['text_on_dark']};
                font-size: 18px;
                font-weight: 600;
                padding: 6px 0;
            }}
        """
    elif variant == 'section':
        return f"""
            QLabel {{
                color: {COLORS['text_on_dark']};
                font-size: 16px;
                font-weight: 600;
                padding: 4px 0;
                text-transform: uppercase;
                letter-spacing: 1px;
            }}
        """
    elif variant == 'secondary':
        return f"""
            QLabel {{
                color: {COLORS['text_secondary']};
                font-size: 13px;
                padding: 2px 0;
            }}
        """
    else:  # body
        return f"""
            QLabel {{
                color: {COLORS['text_on_dark']};
                font-size: 14px;
                padding: 2px 0;
                line-height: 1.5;
            }}
        """


def get_checkbox_style():
    """Checkbox style"""
    return f"""
        QCheckBox {{
            color: {COLORS['text_on_dark']};
            font-size: 14px;
            spacing: 8px;
        }}
        
        QCheckBox::indicator {{
            width: 20px;
            height: 20px;
            border-radius: 6px;
            border: 2px solid {COLORS['surface_elev']};
            background-color: {COLORS['surface_light']};
        }}
        
        QCheckBox::indicator:hover {{
            border-color: {COLORS['teal']};
        }}
        
        QCheckBox::indicator:checked {{
            background-color: {COLORS['teal']};
            border-color: {COLORS['teal']};
            image: url(none);
        }}
        
        QCheckBox::indicator:checked:hover {{
            background-color: {COLORS['cyan']};
            border-color: {COLORS['cyan']};
        }}
    """


def get_line_edit_style():
    """Line edit (text input) style"""
    return f"""
        QLineEdit {{
            background-color: {COLORS['surface_light']};
            color: {COLORS['text_on_dark']};
            border: 1px solid {COLORS['surface_elev']};
            border-radius: 8px;
            padding: 10px 12px;
            font-size: 14px;
        }}
        
        QLineEdit:focus {{
            border-color: {COLORS['teal']};
        }}
        
        QLineEdit:read-only {{
            background-color: {COLORS['surface_elev']};
            color: {COLORS['text_secondary']};
        }}
    """


def get_scroll_area_style():
    """Scroll area style"""
    return f"""
        QScrollArea {{
            background-color: transparent;
            border: none;
        }}
        
        QScrollBar:vertical {{
            background-color: {COLORS['surface_light']};
            width: 10px;
            border-radius: 5px;
            margin: 0;
        }}
        
        QScrollBar::handle:vertical {{
            background-color: {COLORS['surface_elev']};
            border-radius: 5px;
            min-height: 20px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background-color: {COLORS['teal']};
        }}
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}
        
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
            background: none;
        }}
    """


def get_progress_bar_style():
    """Progress bar style"""
    return f"""
        QProgressBar {{
            background-color: {COLORS['surface_light']};
            border: none;
            border-radius: 4px;
            height: 8px;
            text-align: center;
        }}
        
        QProgressBar::chunk {{
            background-color: qlineargradient(
                x1:0, y1:0, x2:1, y2:0,
                stop:0 {COLORS['teal']},
                stop:1 {COLORS['cyan']}
            );
            border-radius: 4px;
        }}
    """


def get_separator_style():
    """Horizontal separator line"""
    return f"""
        QFrame[frameShape="4"] {{
            background-color: {COLORS['surface_elev']};
            max-height: 1px;
            border: none;
        }}
    """
