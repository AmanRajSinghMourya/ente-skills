// Builds the APNs payloads for Apple's Push Notifications Console, encrypted to
// one phone's registered notification public key. Mirrors the server's
// sendAlbumShare (HPKE X-Wing, HKDF-SHA256, ChaCha20Poly1305, info "ente-push",
// plaintext {"eventType":"album_shared"}); FCM moves data keys next to aps.
// Keep this in sync with server/pkg/controller/push.go when it changes.
//
//	go run . <base64 public key> <out dir>
package main

import (
	"crypto/hpke"
	"encoding/base64"
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
)

// The visible alert is a marker: if the phone shows it, the NSE did not run.
var marker = map[string]any{"title": "RAW-APNS", "body": "NSE did not run"}

func main() {
	if len(os.Args) != 3 {
		fmt.Fprintln(os.Stderr, "usage: go run . <base64 public key> <out dir>")
		os.Exit(2)
	}
	pub, err := base64.StdEncoding.DecodeString(os.Args[1])
	check(err)
	if len(pub) != 1216 {
		check(fmt.Errorf("public key is %d bytes, want 1216", len(pub)))
	}
	publicKey, err := hpke.MLKEM768X25519().NewPublicKey(pub)
	check(err)
	ciphertext, err := hpke.Seal(publicKey, hpke.HKDFSHA256(), hpke.ChaCha20Poly1305(),
		[]byte("ente-push"), []byte(`{"eventType":"album_shared"}`))
	check(err)
	valid := base64.StdEncoding.EncodeToString(ciphertext)
	check(os.MkdirAll(os.Args[2], 0o755))
	write("valid", valid)
	write("garbage", "Z2FyYmFnZQ==")
	write("plain", "")
	fmt.Printf("wrote %s/payload-{valid,garbage,plain}.json ciphertext chars: %d\n", os.Args[2], len(valid))
}

func write(name, ciphertext string) {
	payload := map[string]any{"aps": map[string]any{
		"alert": marker, "mutable-content": 1, "sound": "default",
	}}
	if ciphertext != "" {
		payload["notificationCiphertext"] = ciphertext
	}
	out, err := json.MarshalIndent(payload, "", "  ")
	check(err)
	check(os.WriteFile(filepath.Join(os.Args[2], "payload-"+name+".json"), out, 0o600))
}

func check(err error) {
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}
