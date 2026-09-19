export const baseURL = (__ENV.BASE_URL || 'http://127.0.0.1:8765').replace(/\/$/, '');
if (!/^https?:\/\/(localhost|127\.0\.0\.1)(:\d+)?$/.test(baseURL) && __ENV.ALLOW_REMOTE_TARGET !== 'true') {
  throw new Error('Remote targets require explicit ALLOW_REMOTE_TARGET=true');
}
export const suite = __ENV.SUITE || 'checkout';
export const profile = __ENV.PROFILE || 'smoke';
export const users = JSON.parse(open('../users.json'));
const vus = Number(__ENV.VUS || (profile === 'smoke' ? 1 : 3));
if (!Number.isInteger(vus) || vus < 1 || vus > users.length) throw new Error('VUS must fit the 20-user synthetic pool');
if (!['login', 'catalog', 'checkout'].includes(suite)) throw new Error('Unknown suite');
if (!['smoke', 'baseline', 'load'].includes(profile)) throw new Error('Unknown profile');
const workload = profile === 'smoke'
  ? { executor: 'per-vu-iterations', vus, iterations: 1, maxDuration: '30s' }
  : profile === 'baseline'
    ? { executor: 'constant-vus', vus, duration: '30s' }
    : { executor: 'ramping-vus', startVUs: 0, stages: [
        { duration: '10s', target: vus }, { duration: '30s', target: vus }, { duration: '10s', target: 0 }
      ], gracefulRampDown: '10s' };
export const options = {
  scenarios: { sample_store: workload },
  thresholds: {
    checks: ['rate>=0.99'], http_req_failed: ['rate<=0.01'],
    journey_success: ['rate>=0.99'], journey_ms: [`p(95)<${Number(__ENV.P95_MS || 2000)}`]
  },
  systemTags: ['status', 'method', 'name', 'scenario', 'expected_response'],
  summaryTrendStats: ['min', 'avg', 'med', 'p(90)', 'p(95)', 'max'],
};
