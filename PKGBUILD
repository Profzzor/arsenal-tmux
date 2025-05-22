# Maintainer: profzzor <https://github.com/profzzor>

pkgname=arsenal-tmux
pkgver=1.0.0
pkgrel=1
pkgdesc="Tmux-integrated fork of arsenal-cli (pentest command launcher)"
arch=('any')
url="https://github.com/profzzor/arsenal-tmux"
license=('GPL3')
depends=(
  'python'
  'python-libtmux'
  'python-pyperclip'
  'python-docutils'
  'python-pyyaml'
  'python-pyfzf'
)
makedepends=('python-build' 'python-installer' 'python-wheel' 'python-setuptools')
source=("local::$PWD")
noextract=()
sha512sums=('SKIP')

build() {
    cd "$srcdir"
    python -m build --wheel --no-isolation
}

package() {
    cd "$srcdir"
    python -m installer --destdir="$pkgdir" dist/*.whl
}