package com.vibevault;

import com.vibevault.dto.PlaylistDTO;
import com.vibevault.dto.SongCreateDTO;
import com.vibevault.model.Playlist;
import com.vibevault.model.User;
import com.vibevault.repository.PlaylistRepository;
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
 * 公开 PlaylistService 集成测试
 * 
 * 这些测试需要启动 Spring 上下文，用于验证 Service 层的基本功能。
 * 注意：隐藏测试会检查更多边界条件！
 * 
 * 提示：这些测试需要你先完成以下工作才能运行：
 * 1. 为实体类添加 JPA 注解
 * 2. 实现 Repository 方法
 * 3. 实现 PlaylistServiceImpl 中的方法
 */
@SpringBootTest
@ActiveProfiles("test")
@Transactional
class PublicPlaylistServiceTest {

    @Autowired
    private PlaylistService playlistService;

    @Autowired
    private PlaylistRepository playlistRepository;

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private PasswordEncoder passwordEncoder;

    private User testUser;

    @BeforeEach
    void setUp() {
        testUser = new User("testuser", passwordEncoder.encode("password123"));
        userRepository.save(testUser);
    }

    @Test
    @DisplayName("getAllPlaylists 应该返回所有歌单")
    void getAllPlaylists_shouldReturnAllPlaylists() {
        // Given
        Playlist playlist1 = new Playlist("My Favorites", testUser);
        Playlist playlist2 = new Playlist("Workout Mix", testUser);
        playlistRepository.save(playlist1);
        playlistRepository.save(playlist2);

        // When
        List<PlaylistDTO> playlists = playlistService.getAllPlaylists();

        // Then
        assertNotNull(playlists);
        assertTrue(playlists.size() >= 2, "Should return at least 2 playlists");
    }

    @Test
    @DisplayName("getPlaylistById 应该返回正确的歌单")
    void getPlaylistById_shouldReturnCorrectPlaylist() {
        // Given
        Playlist playlist = new Playlist("Test Playlist", testUser);
        playlist = playlistRepository.save(playlist);

        // When
        PlaylistDTO result = playlistService.getPlaylistById(playlist.getId());

        // Then
        assertNotNull(result);
        assertEquals("Test Playlist", result.name());
        assertEquals("testuser", result.ownerUsername());
    }

    @Test
    @DisplayName("createPlaylist 应该创建新歌单")
    void createPlaylist_shouldCreateNewPlaylist() {
        // When
        PlaylistDTO result = playlistService.createPlaylist("New Playlist", "testuser");

        // Then
        assertNotNull(result);
        assertNotNull(result.id());
        assertEquals("New Playlist", result.name());
        assertEquals("testuser", result.ownerUsername());
    }

    @Test
    @DisplayName("addSongToPlaylist 应该向歌单添加歌曲")
    void addSongToPlaylist_shouldAddSong() {
        // Given
        PlaylistDTO playlist = playlistService.createPlaylist("My Playlist", "testuser");
        SongCreateDTO song = new SongCreateDTO("Test Song", "Test Artist", 180);

        // When
        playlistService.addSongToPlaylist(playlist.id(), song, "testuser");

        // Then
        PlaylistDTO updated = playlistService.getPlaylistById(playlist.id());
        assertEquals(1, updated.songs().size());
        assertEquals("Test Song", updated.songs().get(0).title());
    }
}
