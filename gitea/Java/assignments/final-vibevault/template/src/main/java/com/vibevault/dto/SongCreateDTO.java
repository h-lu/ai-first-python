package com.vibevault.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.PositiveOrZero;

public record SongCreateDTO(
    @NotBlank(message = "Song title is required")
    String title,
    
    @NotBlank(message = "Artist name is required")
    String artist,
    
    @PositiveOrZero(message = "Duration must be non-negative")
    int durationInSeconds
) {
}
