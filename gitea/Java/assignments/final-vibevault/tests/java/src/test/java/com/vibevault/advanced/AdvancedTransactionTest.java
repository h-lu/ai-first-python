package com.vibevault.advanced;

import com.vibevault.dto.PlaylistDTO;
import com.vibevault.dto.SongCreateDTO;
import com.vibevault.model.User;
import com.vibevault.repository.UserRepository;
import com.vibevault.service.PlaylistService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Advanced 轨道测试：事务与一致性
 */
@SpringBootTest
@ActiveProfiles("test")
@Transactional
class AdvancedTransactionTest {

    @Autowired
    private PlaylistService playlistService;

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private PasswordEncoder passwordEncoder;

    private User testUser;

    @BeforeEach
    void setUp() {
        testUser = userRepository.save(new User("testuser", passwordEncoder.encode("password")));
    }

    @Test
    @DisplayName("批量添加歌曲应该是原子操作")
    void batchAddSongs_shouldBeAtomic() {
        PlaylistDTO playlist = playlistService.createPlaylist("Test Playlist", "testuser");
        List<SongCreateDTO> songs = List.of(
                new SongCreateDTO("Song 1", "Artist 1", 180),
                new SongCreateDTO("Song 2", "Artist 2", 200),
                new SongCreateDTO("Song 3", "Artist 3", 220)
        );

        for (SongCreateDTO song : songs) {
            playlistService.addSongToPlaylist(playlist.id(), song, "testuser");
        }

        PlaylistDTO updated = playlistService.getPlaylistById(playlist.id());
        assertEquals(3, updated.songs().size());
    }

    @Test
    @DisplayName("创建歌单后应该能立即查询到")
    void createPlaylist_shouldBeImmediatelyVisible() {
        PlaylistDTO created = playlistService.createPlaylist("Immediate Playlist", "testuser");

        PlaylistDTO found = playlistService.getPlaylistById(created.id());
        assertNotNull(found);
        assertEquals("Immediate Playlist", found.name());
    }

    @Test
    @DisplayName("删除歌单后应该立即无法查询")
    void deletePlaylist_shouldBeImmediatelyEffective() {
        PlaylistDTO playlist = playlistService.createPlaylist("To Delete", "testuser");

        playlistService.deletePlaylist(playlist.id(), "testuser");

        assertThrows(Exception.class, () -> {
            playlistService.getPlaylistById(playlist.id());
        });
    }
}
