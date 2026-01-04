package com.vibevault.dto;

public record SongDTO(
    Long id,
    String title,
    String artist,
    int durationInSeconds
) {
}
