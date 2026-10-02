// RUN: %verify "%s" > "%t"
// RUN: %diff "%s.expect" "%t"

// Every item of a map or imap is a pair, so these hold.

method MapItems() {
  assert map[1 := 2].Items == {(1, 2)};
}

method IMapItems() {
  assert imap[1 := 2].Items == iset{(1, 2)};
}
