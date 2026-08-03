import http.server
import socket
import sys
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

PORT = 8080

def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('223.5.5.5', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return 'localhost'

ip = get_ip()
url = f'http://{ip}:{PORT}/wish.html'

# 生成 ASCII 二维码（终端可见）
qr_str = url
size = 21
# 用字符画粗略展示链接
print(f'''
╔══════════════════════════════════════════╗
║      🌠  许愿星愿 已启动  🌠           ║
╠══════════════════════════════════════════╣
║                                          ║
║  📱 手机浏览器打开：                     ║
║  {url}
║                                          ║
║  📤 微信分享：把这个链接复制到微信       ║
║  对方点击即可在浏览器中打开              ║
║                                          ║
║  按 Ctrl+C 关闭                          ║
╚══════════════════════════════════════════╝
''')

# 尝试生成二维码图片
try:
    import qrcode
    qr = qrcode.QRCode(box_size=10, border=2)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color='#6b7fff', back_color='#060618')
    qr_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'wish_qr.png')
    img.save(qr_path)
    print(f'  🖼️  二维码已保存: {qr_path}')
    print(f'  把这张图发到微信，对方长按识别即可打开')
except ImportError:
    print(f'  💡 提示: pip install qrcode[pil] 后可生成二维码图片')

print()

Handler = http.server.SimpleHTTPRequestHandler
Handler.extensions_map['.html'] = 'text/html; charset=utf-8'

with http.server.HTTPServer(('0.0.0.0', PORT), Handler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('\n服务器已关闭')
