package com.vibevault.dto;

import java.util.List;

public record PlaylistDTO(
    Long id,
    String name,
    String ownerUsername,
    List<SongDTO> songs
) {
}
