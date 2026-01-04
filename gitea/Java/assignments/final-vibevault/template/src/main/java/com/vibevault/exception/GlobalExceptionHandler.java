package com.vibevault.exception;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import org.springframework.web.server.ResponseStatusException;

import java.time.LocalDateTime;
import java.util.Map;

/**
 * 全局异常处理器
 * 
 * 需要实现：
 * - 捕获 ResourceNotFoundException 并返回 404 状态码
 * - 捕获 UnauthorizedException 并返回 403 状态码
 * - 捕获 ResponseStatusException 并返回对应状态码
 * - [Advanced] 统一处理其他异常，返回合适的错误响应格式
 */
@RestControllerAdvice
public class GlobalExceptionHandler {

    // TODO: 实现 ResourceNotFoundException 处理器 (返回 404)

    // TODO: 实现 UnauthorizedException 处理器 (返回 403)

    // TODO: 实现 ResponseStatusException 处理器

    // TODO [Advanced]: 实现通用异常处理器
}
