/**
 * Aetas Claude API Proxy Worker
 * Deployed at: aetas-wealth.com/api/claude
 * Stores CLAUDE_API_KEY as a Worker secret (never in code)
 * Allows the Content Agent to call Claude from the browser without CORS issues
 */

export default {
  async fetch(request, env) {

    // CORS preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        status: 204,
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'POST, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type',
          'Access-Control-Max-Age': '86400',
        }
      });
    }

    // Only allow POST
    if (request.method !== 'POST') {
      return new Response('Method not allowed', { status: 405 });
    }

    // Validate origin — only allow requests from Aetas domains
    const origin = request.headers.get('Origin') || '';
    const allowed = [
      'https://aetas-wealth.com',
      'https://workplace.aetas-wealth.com',
      'https://charities.aetas-wealth.com',
      'http://localhost',
      'file://'
    ];
    const isAllowed = allowed.some(o => origin.startsWith(o)) || origin === '';
    if (!isAllowed) {
      return new Response('Forbidden', { status: 403 });
    }

    // Parse body
    let body;
    try {
      body = await request.json();
    } catch {
      return new Response('Invalid JSON', { status: 400 });
    }

    // Forward to Anthropic API using stored secret key
    const anthropicRes = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': env.CLAUDE_API_KEY,
        'anthropic-version': '2023-06-01',
      },
      body: JSON.stringify({
        model: body.model || 'claude-sonnet-4-6',
        max_tokens: body.max_tokens || 4000,
        system: body.system || '',
        messages: body.messages || [],
      })
    });

    const data = await anthropicRes.json();

    return new Response(JSON.stringify(data), {
      status: anthropicRes.status,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      }
    });
  }
};
