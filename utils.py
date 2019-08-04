def within_rect(x, y, rect):
    return rect.x <= x <= rect.x + rect.width and rect.y <= y <= rect.y + rect.height
