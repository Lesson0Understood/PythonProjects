def darken_color(hex_color, factor=0.2):
    # Convert hex color to RGB
    hex_color = hex_color.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    # Darken the color
    darkened_rgb = tuple(max(0, int(c * (1 - factor))) for c in rgb)

    # Convert back to hex
    return '#{:02x}{:02x}{:02x}'.format(*darkened_rgb)

# Example usage
original_color = "#2B3E50"
darkened_color = darken_color(original_color, 0.1)
print(darkened_color)  # Output: #273848
