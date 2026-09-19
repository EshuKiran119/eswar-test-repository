import http from 'k6/http';
import { check, sleep } from 'k6';
import exec from 'k6/execution';
import { Trend, Rate } from 'k6/metrics';
import { baseURL, suite, users, options as configuration } from './config.js';
export const options = configuration;
const elapsed = new Trend('journey_ms', true);
const success = new Rate('journey_success');
function request(method, path, body, token, name) {
  return http.request(method, `${baseURL}${path}`, body === null ? null : JSON.stringify(body), {
    headers: { 'Content-Type': 'application/json', ...(token ? { Authorization: `Bearer ${token}` } : {}) },
    timeout: '5s', tags: { name },
  });
}
function verify(response, status, predicate, label) {
  let data = null;
  try { data = response.json(); } catch (_) { /* Non-JSON fails semantic checks. */ }
  const valid = check(response, { [label]: () => response.status === status && predicate(data) });
  if (!valid) throw new Error(`Contract failed: ${label}; HTTP ${response.status}`);
  return data;
}
export default function () {
  const user = users[(exec.vu.idInTest - 1) % users.length];
  let token = '', order = '', passed = false;
  const start = Date.now();
  try {
    const login = verify(request('POST', '/api/login', user, '', 'login'), 200,
      d => d && typeof d.token === 'string' && d.token.length > 0 && d.username === user.username, 'login contract');
    token = login.token;
    if (suite !== 'login') {
      verify(request('GET', '/api/products', null, token, 'catalog'), 200,
        d => d && d.products.some(p => p.sku === 'notebook' && p.price_cents === 1250), 'catalog contract');
    }
    if (suite === 'checkout') {
      const createdResponse = request('POST', '/api/orders', { sku: 'notebook', quantity: 2 }, token, 'create order');
      // Retain the resource identifier before asserting, so failed mappings can still be cleaned up.
      try { order = createdResponse.json().id || ''; } catch (_) {}
      verify(createdResponse, 201,
        d => d && d.id && d.owner === user.username && d.quantity === 2 && d.total_cents === 2500, 'order mapping');
      verify(request('GET', `/api/orders/${order}`, null, token, 'read order'), 200,
        d => d && d.id === order && d.total_cents === 2500 && d.sku === 'notebook', 'persisted mapping');
    }
    passed = true;
  } catch (error) {
    console.error(error.message); // Never log headers, tokens, credentials or response bodies.
  } finally {
    elapsed.add(Date.now() - start, { suite });
    success.add(passed, { suite });
    if (token && order) check(request('DELETE', `/api/orders/${order}`, null, token, 'cleanup order'), { 'cleanup order': r => r.status === 204 });
    if (token) check(request('POST', '/api/logout', {}, token, 'cleanup session'), { 'cleanup session': r => r.status === 204 });
  }
  sleep(0.25); // Pacing and cleanup are outside journey_ms.
}
export function handleSummary(data) {
  return { [__ENV.SUMMARY_PATH || 'summary.json']: JSON.stringify(data, null, 2) };
}
