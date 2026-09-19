// One synthetic identity per thread; no real accounts or application data.
int number = ctx.getThreadNum() + 1
if (number > 20) throw new IllegalArgumentException('The demo pool supports at most 20 users')
vars.put('username', String.format('sample%02d', number))
vars.put('password', String.format('DemoOnly%02d!', number))
vars.put('token', '')
vars.put('order_id', '')
