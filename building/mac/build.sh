export PATH=/usr/local/qt5/5.4/clang_64/bin:$PATH

# Then in denarius-qt.pro you'll want to change deployment Target to 10.9
# and change your sdk to your macOS SDK and then run

qmake "USE_UPNP=1" "USE_QRCODE=1" "USE_LEVELDB=1" denarius-qt.pro
# make -I/usr/local/Cellar/boost@1.57/1.57.0/include -I/usr/local/opt/openssl/include
make
