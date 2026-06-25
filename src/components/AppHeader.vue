<template>
  <nav>
    <div class="wrap nav-inner">
      <div class="nav-logo">
        <img src="https://secureitlab.com/assets/images/secureitlab-logo.png" alt="SecureITLab">
      </div>
      <a href="#quote" class="nav-cta">Get My Quote →</a>
    </div>
  </nav>
</template>

<style scoped>
nav {
  position: sticky;
  top: 0;
  z-index: 50;
  background: rgba(255,255,255,0.97);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid #E5E7EB;
  box-shadow: 0 1px 4px rgba(0,0,0,.07), 0 1px 2px rgba(0,0,0,.04);
}
.nav-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 70px;
}
.wrap {
  max-width: 1160px;
  margin: 0 auto;
  padding: 0 32px;
}
.nav-logo { display: flex; align-items: center; }
.nav-logo img { height: 38px; width: auto; display: block; }

.nav-cta {
  font-family: 'Montserrat', sans-serif;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.03em;
  padding: 11px 26px;
  background: #F5C400;
  color: #0D2E5E;
  border-radius: 50px;
  transition: background 0.2s;
  white-space: nowrap;
  text-decoration: none;
}
.nav-cta:hover { background: #D4A900; }

@media (max-width: 560px) {
  .nav-cta { font-size: 12px; padding: 9px 18px; }
  .wrap { padding: 0 20px; }
}
</style>
