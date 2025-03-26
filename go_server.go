package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"log"
	"os"
	"path/filepath"
	"time"
)

// 请求结构体
type Request struct {
	JSONRPC string                 `json:"jsonrpc"`
	ID      interface{}            `json:"id"`
	Method  string                 `json:"method"`
	Params  map[string]interface{} `json:"params"`
}

// 响应结构体
type Response struct {
	JSONRPC string      `json:"jsonrpc"`
	ID      interface{} `json:"id"`
	Result  interface{} `json:"result,omitempty"`
	Error   *Error      `json:"error,omitempty"`
}

// 错误结构体
type Error struct {
	Code    int    `json:"code"`
	Message string `json:"message"`
}

func main() {
	// 设置日志
	logDir := filepath.Join(os.Getenv("HOME"), ".mcp-logs")
	os.MkdirAll(logDir, 0755)
	logFile := filepath.Join(logDir, fmt.Sprintf("mcp_go_%d.log", time.Now().Unix()))
	f, err := os.Create(logFile)
	if err != nil {
		fmt.Fprintf(os.Stderr, "无法创建日志文件: %v\n", err)
		os.Exit(1)
	}
	defer f.Close()
	
	log.SetOutput(f)
	log.SetFlags(log.Ldate | log.Ltime | log.Lmicroseconds)
	
	log.Println("Go MCP 服务器启动")
	
	// 创建缓冲读取器
	scanner := bufio.NewScanner(os.Stdin)
	
	// 主循环
	for scanner.Scan() {
		line := scanner.Text()
		log.Printf("收到输入: %s", line)
		
		// 解析请求
		var request Request
		if err := json.Unmarshal([]byte(line), &request); err != nil {
			log.Printf("JSON解析错误: %v", err)
			sendErrorResponse(nil, -32700, "Parse error: Invalid JSON")
			continue
		}
		
		log.Printf("处理请求: method=%s, id=%v", request.Method, request.ID)
		
		// 处理不同的方法
		switch request.Method {
		case "initialize":
			response := Response{
				JSONRPC: "2.0",
				ID:      request.ID,
				Result: map[string]interface{}{
					"name":    "go-mcp-server",
					"version": "1.0.0",
					"capabilities": map[string]interface{}{
						"tools": map[string]interface{}{},
					},
				},
			}
			
			sendResponse(response)
			
		case "list_tools":
			tools := []map[string]interface{}{
				{
					"name":        "hello_world",
					"description": "A simple hello world function",
					"inputSchema": map[string]interface{}{
						"type": "object",
						"properties": map[string]interface{}{
							"name": map[string]interface{}{
								"type":        "string",
								"description": "Your name",
							},
						},
					},
				},
			}
			
			response := Response{
				JSONRPC: "2.0",
				ID:      request.ID,
				Result: map[string]interface{}{
					"tools": tools,
				},
			}
			
			sendResponse(response)
			
		case "call_tool":
			name := ""
			if params, ok := request.Params["name"].(string); ok {
				name = params
			}
			
			args := make(map[string]interface{})
			if a, ok := request.Params["arguments"].(map[string]interface{}); ok {
				args = a
			}
			
			if name == "hello_world" {
				userName := "World"
				if n, ok := args["name"].(string); ok {
					userName = n
				}
				
				response := Response{
					JSONRPC: "2.0",
					ID:      request.ID,
					Result: map[string]interface{}{
						"content": []map[string]interface{}{
							{
								"type": "text",
								"text": fmt.Sprintf("Hello, %s!", userName),
							},
						},
					},
				}
				
				sendResponse(response)
			} else {
				sendErrorResponse(request.ID, -32601, fmt.Sprintf("Tool not found: %s", name))
			}
			
		default:
			sendErrorResponse(request.ID, -32601, fmt.Sprintf("Method not found: %s", request.Method))
		}
	}
	
	if err := scanner.Err(); err != nil {
		log.Printf("扫描器错误: %v", err)
	}
	
	log.Println("服务器退出")
}

// 发送响应
func sendResponse(response Response) {
	responseJSON, err := json.Marshal(response)
	if err != nil {
		log.Printf("JSON序列化错误: %v", err)
		sendErrorResponse(response.ID, -32603, "Internal error: Failed to serialize response")
		return
	}
	
	log.Printf("发送响应: %s", string(responseJSON))
	
	// 写入标准输出并刷新
	fmt.Println(string(responseJSON))
	
	log.Printf("响应已发送")
}

// 发送错误响应
func sendErrorResponse(id interface{}, code int, message string) {
	response := Response{
		JSONRPC: "2.0",
		ID:      id,
		Error: &Error{
			Code:    code,
			Message: message,
		},
	}
	
	responseJSON, err := json.Marshal(response)
	if err != nil {
		log.Printf("错误响应序列化失败: %v", err)
		return
	}
	
	log.Printf("发送错误响应: %s", string(responseJSON))
	
	// 写入标准输出并刷新
	fmt.Println(string(responseJSON))
	
	log.Printf("错误响应已发送")
}
