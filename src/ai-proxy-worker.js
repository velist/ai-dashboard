/**
 * Cloudflare Worker - AI 对话代理
 * 用于安全地转发硅基流动API请求，隐藏API Key
 */

export default {
  async fetch(request, env, ctx) {
    // 获取请求头中的Origin，用于CORS验证
    const origin = request.headers.get('Origin');

    // 处理OPTIONS预检请求
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        headers: {
          'Access-Control-Allow-Origin': origin || '*',
          'Access-Control-Allow-Methods': 'POST, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type',
          'Access-Control-Max-Age': '86400',
        },
      });
    }

    // 只处理 POST 请求
    if (request.method !== 'POST') {
      return new Response('Method not allowed', { status: 405 });
    }

    // 允许的域名列表
    const allowedOrigins = [
      'https://bltestdata.aipush.fun',
      'https://ai-dashboard-6p0.pages.dev',
      'http://localhost:3000',
      'http://localhost:8000'
    ];

    // 简单的CORS检查
    const isAllowed = allowedOrigins.some(allowed =>
      origin && (origin === allowed || origin.includes('ai-dashboard-6p0.pages.dev'))
    );

    if (!isAllowed && origin) {
      console.log(`Rejected request from origin: ${origin}`);
      return new Response('Forbidden', { status: 403 });
    }

    try {
      // 获取请求体
      const requestBody = await request.json();

      // 转发请求到硅基流动API
      const response = await fetch('https://api.siliconflow.cn/v1/chat/completions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${env.SILICONFLOW_API_KEY}`,
        },
        body: JSON.stringify(requestBody),
      });

      // 获取响应内容
      const responseData = await response.json();

      // 构建响应头（包含CORS）
      const responseHeaders = new Headers({
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': origin || '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
      });

      // 返回代理响应
      return new Response(JSON.stringify(responseData), {
        status: response.status,
        headers: responseHeaders,
      });

    } catch (error) {
      console.error('Worker error:', error);
      return new Response(JSON.stringify({
        error: 'Internal server error',
        message: error.message,
      }), {
        status: 500,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': origin || '*',
        },
      });
    }
  }
};
