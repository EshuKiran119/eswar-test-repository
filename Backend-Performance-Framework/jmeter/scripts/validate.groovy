import groovy.json.JsonSlurper
// The sampler label is a stable contract identifier. Do not log response bodies.
try {
    String label = prev.getSampleLabel()
    int status = Integer.parseInt(prev.getResponseCode())
    if (label.startsWith('CLEANUP')) { assert status == 204; return }
    def data = new JsonSlurper().parseText(prev.getResponseDataAsString())
    switch (label) {
        case 'API | login':
            assert status == 200
            assert data.token instanceof String && !data.token.empty
            vars.put('token', data.token)
            assert data.username == vars.get('username')
            break
        case 'API | catalog':
            assert status == 200
            assert data.products.any { it.sku == 'notebook' && it.price_cents == 1250 }
            break
        case 'API | create-order':
            if (data.id) vars.put('order_id', data.id.toString())
            assert status == 201
            assert data.owner == vars.get('username')
            assert data.quantity == 2 && data.total_cents == 2500
            break
        case 'API | read-order':
            assert status == 200
            assert data.id == vars.get('order_id') && data.sku == 'notebook'
            assert data.total_cents == 2500
            break
        default: throw new IllegalArgumentException('Unknown contract label')
    }
} catch (Throwable error) {
    prev.setSuccessful(false)
    prev.setResponseMessage('Contract assertion failed: ' + error.class.simpleName)
}
