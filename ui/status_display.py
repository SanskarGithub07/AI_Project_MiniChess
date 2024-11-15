import pygame

class StatusDisplay:
    def __init__(self, board_width, board_height, sidebar_width):
        self.board_width = board_width
        self.board_height = board_height
        self.sidebar_width = sidebar_width
        
        # Status display configuration
        self.status_height = 140
        self.padding = 10
        
        # Position in middle of sidebar
        self.x_position = board_width + self.padding
        self.y_position = (board_height // 2) - (self.status_height // 2)
        
        # Font setup
        self.title_font_size = 22
        self.message_font_size = 18
        self.action_font_size = 16
        self.title_font = pygame.font.SysFont("Arial", self.title_font_size, bold=True)
        self.message_font = pygame.font.SysFont("Segoe UI", self.message_font_size, bold=True)
        self.action_font = pygame.font.SysFont("Segoe UI", self.action_font_size, bold=True)
        
        # Colors
        self.colors = {
            'normal': {
                'bg': (248, 250, 252),
                'border': (226, 232, 240),
                'text': (15, 23, 42)
            },
            'check': {
                'bg': (254, 243, 199),
                'border': (251, 191, 36),
                'text': (146, 64, 14)
            },
            'checkmate': {
                'bg': (254, 226, 226),
                'border': (239, 68, 68),
                'text': (153, 27, 27)
            },
            'stalemate': {
                'bg': (241, 245, 249),
                'border': (148, 163, 184),
                'text': (51, 65, 85)
            }
        }
        
        self.current_message = ""
        self.checking_piece = ""  # New attribute to store the checking piece info
        self.message_type = "normal"
        self.display_time = 2000
        self.message_start_time = 0
        self.should_display = False

    def update_status(self, message, message_type="normal", checking_piece=None):
        if message != self.current_message or message_type == "check":
            self.current_message = message
            self.message_type = message_type
            self.checking_piece = checking_piece  # Store checking piece info
            self.message_start_time = pygame.time.get_ticks()
            self.should_display = True

    def draw(self, screen):
        if not self.should_display or not self.current_message:
            return
        
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.message_start_time
        
        if elapsed > self.display_time and self.message_type not in ['checkmate', 'stalemate']:
            self.should_display = False
            self.current_message = ""
            return
        
        # Create status box
        status_rect = pygame.Rect(
            self.x_position,
            self.y_position,
            self.sidebar_width - (self.padding * 2),
            self.status_height
        )
        
        color_scheme = self.colors[self.message_type]
        
        # Draw shadow
        shadow_rect = status_rect.copy()
        shadow_rect.move_ip(2, 2)
        pygame.draw.rect(screen, (0, 0, 0, 30), shadow_rect, border_radius=10)
        
        # Draw main background with rounded corners
        pygame.draw.rect(screen, color_scheme['bg'], status_rect, border_radius=10)
        pygame.draw.rect(screen, color_scheme['border'], status_rect, 2, border_radius=10)
        
        # Draw title
        title_text = self.get_title_text()
        title_surface = self.title_font.render(title_text, True, color_scheme['text'])
        title_rect = title_surface.get_rect(
            centerx=status_rect.centerx,
            top=status_rect.top + self.padding
        )
        screen.blit(title_surface, title_rect)
        
        # Draw separator
        separator_y = title_rect.bottom + 5
        pygame.draw.line(
            screen,
            color_scheme['border'],
            (status_rect.left + self.padding, separator_y),
            (status_rect.right - self.padding, separator_y),
            1
        )
        
        # Message area
        message_box_height = status_rect.height - separator_y - (self.padding * 3)
        if self.message_type in ['checkmate', 'check']:
            # Reserve space for action text
            message_box_height -= self.action_font.get_linesize() * 2
        
        message_box_rect = pygame.Rect(
            status_rect.left + self.padding * 2,
            separator_y + 10,
            status_rect.width - (self.padding * 4),
            message_box_height
        )
        
        # Draw message
        message_height = self.draw_wrapped_text(
            screen,
            self.current_message,
            self.message_font,
            color_scheme['text'],
            message_box_rect
        )
        
        # Add action text for checkmate and check with wrapping
        if self.message_type == 'checkmate':
            action_box_rect = pygame.Rect(
                status_rect.left + self.padding,
                message_box_rect.top + self.padding,
                status_rect.width - (self.padding * 2),
                self.action_font.get_linesize() * 2
            )
            
            self.draw_wrapped_text(
                screen,
                "Go back to main menu to start a new game",
                self.action_font,
                color_scheme['text'],
                action_box_rect
            )
        elif self.message_type == 'check' and self.checking_piece:
            action_box_rect = pygame.Rect(
                status_rect.left + self.padding,
                message_box_rect.top + self.padding,
                status_rect.width - (self.padding * 2),
                self.action_font.get_linesize() * 2
            )
            
            self.draw_wrapped_text(
                screen,
                f"King is being checked by {self.checking_piece}",
                self.action_font,
                color_scheme['text'],
                action_box_rect
            )

    def get_title_text(self):
        titles = {
            'normal': 'Game Status',
            'check': 'Check!',
            'checkmate': 'Checkmate!',
            'stalemate': 'Stalemate'
        }
        return titles.get(self.message_type, 'Game Status')

    def draw_wrapped_text(self, surface, text, font, color, rect):
        """Improved word wrapping function with better spacing control."""
        words = text.split()
        lines = []
        current_line = []
        
        # Calculate maximum width considering padding
        max_width = rect.width - self.padding * 2
        
        for word in words:
            # Try adding the word to the current line
            test_line = ' '.join(current_line + [word])
            test_surface = font.render(test_line, True, color)
            
            if test_surface.get_width() <= max_width:
                current_line.append(word)
            else:
                # If current line has content, add it to lines
                if current_line:
                    lines.append(' '.join(current_line))
                # Start new line with current word
                current_line = [word]
        
        # Add the last line if it has content
        if current_line:
            lines.append(' '.join(current_line))
        
        # Calculate total height needed for all lines
        line_spacing = 1.2  # Slightly increased line spacing
        total_height = len(lines) * (font.get_linesize() * line_spacing)
        current_y = rect.top + (rect.height - total_height) // 2  # Center vertically
        
        # Draw each line
        for line in lines:
            text_surface = font.render(line, True, color)
            text_rect = text_surface.get_rect(
                centerx=rect.centerx,
                top=current_y
            )
            surface.blit(text_surface, text_rect)
            current_y += font.get_linesize() * line_spacing
        return total_height

    def clear(self):
        self.current_message = ""
        self.checking_piece = ""
        self.should_display = False