package com.vibevault.core;

import com.vibevault.dto.PlaylistDTO;
import com.vibevault.dto.SongCreateDTO;
import com.vibevault.exception.ResourceNotFoundException;
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
 * Core 轨道测试：Service 层业务逻辑
 */
@SpringBootTest
@ActiveProfiles("test")
@Transactional
class CoreServiceTest {

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
    @DisplayName("createPlaylist 应该创建并返回新歌单")
    void createPlaylist_shouldCreateAndReturnPlaylist() {
        PlaylistDTO result = playlistService.createPlaylist("New Playlist", "testuser");

        assertNotNull(result);
        assertNotNull(result.id());
        assertEquals("New Playlist", result.name());
        assertEquals("testuser", result.ownerUsername());
        assertTrue(result.songs().isEmpty());
    }

    @Test
    @DisplayName("getAllPlaylists 应该返回所有歌单")
    void getAllPlaylists_shouldReturnAllPlaylists() {
        playlistService.createPlaylist("Playlist 1", "testuser");
        playlistService.createPlaylist("Playlist 2", "testuser");

        List<PlaylistDTO> playlists = playlistService.getAllPlaylists();

        assertTrue(playlists.size() >= 2);
    }

    @Test
    @DisplayName("getPlaylistById 应该返回正确的歌单")
    void getPlaylistById_shouldReturnCorrectPlaylist() {
        PlaylistDTO created = playlistService.createPlaylist("Test Playlist", "testuser");

        PlaylistDTO result = playlistService.getPlaylistById(created.id());

        assertEquals(created.id(), result.id());
        assertEquals("Test Playlist", result.name());
    }

    @Test
    @DisplayName("getPlaylistById 对于不存在的 ID 应该抛出异常")
    void getPlaylistById_shouldThrowForNonExistentId() {
        assertThrows(ResourceNotFoundException.class, () -> {
            playlistService.getPlaylistById(99999L);
        });
    }

    @Test
    @DisplayName("addSongToPlaylist 应该向歌单添加歌曲")
    void addSongToPlaylist_shouldAddSong() {
        PlaylistDTO playlist = playlistService.createPlaylist("My Playlist", "testuser");
        SongCreateDTO song = new SongCreateDTO("Test Song", "Test Artist", 180);

        playlistService.addSongToPlaylist(playlist.id(), song, "testuser");

        PlaylistDTO updated = playlistService.getPlaylistById(playlist.id());
        assertEquals(1, updated.songs().size());
        assertEquals("Test Song", updated.songs().get(0).title());
    }

    @Test
    @DisplayName("deletePlaylist 应该删除歌单")
    void deletePlaylist_shouldRemovePlaylist() {
        PlaylistDTO playlist = playlistService.createPlaylist("To Delete", "testuser");

        playlistService.deletePlaylist(playlist.id(), "testuser");

        assertThrows(ResourceNotFoundException.class, () -> {
            playlistService.getPlaylistById(playlist.id());
        });
    }

    @Test
    @DisplayName("removeSongFromPlaylist 应该从歌单移除歌曲")
    void removeSongFromPlaylist_shouldRemoveSong() {
        PlaylistDTO playlist = playlistService.createPlaylist("My Playlist", "testuser");
        SongCreateDTO song = new SongCreateDTO("Test Song", "Test Artist", 180);
        playlistService.addSongToPlaylist(playlist.id(), song, "testuser");
        
        PlaylistDTO withSong = playlistService.getPlaylistById(playlist.id());
        Long songId = withSong.songs().get(0).id();

        playlistService.removeSongFromPlaylist(playlist.id(), songId, "testuser");

        PlaylistDTO updated = playlistService.getPlaylistById(playlist.id());
        assertTrue(updated.songs().isEmpty());
    }
}
