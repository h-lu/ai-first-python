package com.vibevault;

import com.vibevault.dto.PlaylistDTO;
import com.vibevault.dto.SongDTO;
import com.vibevault.model.Playlist;
import com.vibevault.model.Song;
import com.vibevault.model.User;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

/**
 * 公开冒烟测试
 * 
 * 这些测试对学生可见，用于本地自检。
 * 通过这些测试不代表能拿满分，还有更多隐藏测试。
 * 
 * 注意：这些测试不需要启动 Spring 上下文，可以快速运行。
 */
class PublicSmokeTest {

    @Test
    @DisplayName("User 实体应该能正确创建")
    void user_shouldBeCreatedCorrectly() {
        User user = new User("testuser", "password123");
        
        assertEquals("testuser", user.getUsername());
        assertEquals("password123", user.getPassword());
        assertEquals("ROLE_USER", user.getRole());
    }

    @Test
    @DisplayName("User 实体应该支持自定义角色")
    void user_shouldSupportCustomRole() {
        User admin = new User("admin", "password123", "ROLE_ADMIN");
        
        assertEquals("admin", admin.getUsername());
        assertEquals("ROLE_ADMIN", admin.getRole());
    }

    @Test
    @DisplayName("Playlist 实体应该能正确创建")
    void playlist_shouldBeCreatedCorrectly() {
        User owner = new User("testuser", "password123");
        Playlist playlist = new Playlist("My Favorites", owner);
        
        assertEquals("My Favorites", playlist.getName());
        assertEquals(owner, playlist.getOwner());
        assertNotNull(playlist.getSongs());
        assertTrue(playlist.getSongs().isEmpty());
    }

    @Test
    @DisplayName("Song 实体应该能正确创建")
    void song_shouldBeCreatedCorrectly() {
        Song song = new Song("Test Song", "Test Artist", 180);
        
        assertEquals("Test Song", song.getTitle());
        assertEquals("Test Artist", song.getArtist());
        assertEquals(180, song.getDurationInSeconds());
    }

    @Test
    @DisplayName("PlaylistDTO 应该正确存储数据")
    void playlistDTO_shouldStoreDataCorrectly() {
        SongDTO song = new SongDTO(1L, "Test Song", "Test Artist", 180);
        PlaylistDTO playlist = new PlaylistDTO(1L, "My Favorites", "testuser", List.of(song));
        
        assertEquals(1L, playlist.id());
        assertEquals("My Favorites", playlist.name());
        assertEquals("testuser", playlist.ownerUsername());
        assertEquals(1, playlist.songs().size());
    }

    @Test
    @DisplayName("Playlist.addSong 应该添加歌曲到歌单")
    void playlist_addSong_shouldAddSongToPlaylist() {
        User owner = new User("testuser", "password123");
        Playlist playlist = new Playlist("My Favorites", owner);
        Song song = new Song("Test Song", "Test Artist", 180);
        
        playlist.addSong(song);
        
        // 这个测试会失败直到你实现 addSong 方法
        assertEquals(1, playlist.getSongs().size(), "歌单应该包含 1 首歌曲");
        assertEquals(playlist, song.getPlaylist(), "歌曲的 playlist 应该指向当前歌单");
    }

    @Test
    @DisplayName("Playlist.removeSong 应该从歌单移除歌曲")
    void playlist_removeSong_shouldRemoveSongFromPlaylist() {
        User owner = new User("testuser", "password123");
        Playlist playlist = new Playlist("My Favorites", owner);
        Song song = new Song("Test Song", "Test Artist", 180);
        
        playlist.addSong(song);
        playlist.removeSong(song);
        
        // 这个测试会失败直到你实现 addSong 和 removeSong 方法
        assertTrue(playlist.getSongs().isEmpty(), "歌单应该为空");
        assertNull(song.getPlaylist(), "歌曲的 playlist 应该为 null");
    }
}
