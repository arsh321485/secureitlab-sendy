<script setup lang="ts">
import { onMounted } from 'vue'
import AppHeader from '@/components/AppHeader.vue'

const BASE_URL = import.meta.env.VITE_API_BASE_URL as string

onMounted(() => {
  const UTM_KEYS = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content']
  const params = new URLSearchParams(window.location.search)
  const form = document.getElementById('quoteForm') as HTMLFormElement | null

  if (!form) return

  UTM_KEYS.forEach((key) => {
    const val = params.get(key)
    if (val) {
      const h = document.createElement('input')
      h.type = 'hidden'
      h.name = key
      h.value = val
      form.appendChild(h)
    }
  })

  const success = document.getElementById('formSuccess')
  const errorDiv = document.getElementById('formError')
  const submitBtn = form.querySelector<HTMLButtonElement>('.form-submit')

  form.addEventListener('submit', async (e) => {
    e.preventDefault()

    const required = form.querySelectorAll<HTMLInputElement>('[required]')
    let ok = true
    required.forEach((el) => {
      if (!el.value.trim()) {
        el.style.borderColor = '#DC2626'
        ok = false
      } else {
        el.style.borderColor = ''
      }
    })
    const emailEl = document.getElementById('email') as HTMLInputElement
    if (emailEl.value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(emailEl.value)) {
      emailEl.style.borderColor = '#DC2626'
      ok = false
    }
    if (!ok) return

    const fd = new FormData(form)
    const payload = {
      firstname: fd.get('firstname') as string,
      lastname: fd.get('lastname') as string,
      email: fd.get('email') as string,
      phone: (fd.get('phone') as string) || '',
      company_size: (fd.get('company_size') as string) || '1-50 Employees',
      looking_to_start: (fd.get('looking_to_start') as string) || 'Just Exploring',
    }

    if (submitBtn) { submitBtn.disabled = true; submitBtn.textContent = 'Sending…' }
    if (errorDiv) errorDiv.style.display = 'none'

    try {
      const res = await fetch(`${BASE_URL}/api/enquiry`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      })

      if (!res.ok) {
        const err = await res.json().catch(() => ({}))
        throw new Error((err as any).detail || 'Submission failed. Please try again.')
      }

      form.classList.add('sent')
      success?.classList.add('show')
      success?.scrollIntoView({ behavior: 'smooth', block: 'center' })

      ;(window as any).Swal.fire({
        icon: 'success',
        title: 'Submitted Successfully!',
        text: 'A specialist will be in touch within one business day.',
        confirmButtonText: 'OK',
        confirmButtonColor: '#1B4080',
      })
    } catch (err: unknown) {
      if (errorDiv) {
        errorDiv.textContent = err instanceof Error ? err.message : 'Something went wrong. Please try again.'
        errorDiv.style.display = 'block'
      }
      if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = 'Send My Quote Request →' }
    }
  })
})
</script>

<template>
  <AppHeader />

  <!-- ─── HERO ─── -->
  <header class="hero">
    <div class="wrap hero-grid">
      <div>
        <span class="eyebrow reveal d1">Year-Round Security Bundle</span>
        <h1 class="reveal d2">One package.<br>Full-year <span class="accent">cybersecurity</span> coverage.</h1>
        <p class="lede reveal d2">Most businesses get tested once a year — and stay exposed for the other 364 days. This bundle runs all year: VAPT twice over, ISO 27001 compliance support, quarterly training, and phishing simulation under one engagement.</p>

        <div class="hero-stats reveal d2">
          <div class="hstat"><span class="hstat-n">2×</span><span class="hstat-l">VAPT per year</span></div>
          <div class="hstat-div"></div>
          <div class="hstat"><span class="hstat-n">5</span><span class="hstat-l">Services bundled</span></div>
          <div class="hstat-div"></div>
          <div class="hstat"><span class="hstat-n">1</span><span class="hstat-l">Partner, not five</span></div>
        </div>

        <div class="hero-actions reveal d3">
          <a href="#quote"><button class="btn-prim">Get My Quote →</button></a>
          <span class="hero-note">Under 2 minutes · No obligation · Reply within 1 business day</span>
        </div>
      </div>

      <div class="bundle-card reveal d3">
        <div class="bc-head">
          <span class="bc-title">What's in the bundle</span>
          <span class="bc-tag">5 SERVICES</span>
        </div>
        <div class="bc-line"><span class="tick">✓</span><span><strong>VAPT, twice a year</strong> — up to 25 IPs &amp; 3 web apps</span></div>
        <div class="bc-line"><span class="tick">✓</span><span>Access to <a href="http://vaptfix.ai/" target="_blank" rel="noopener noreferrer" class="vaptfix-link"><strong>VaptFix.ai</strong></a> remediation platform</span></div>
        <div class="bc-line"><span class="tick">✓</span><span><strong>ISO 27001</strong> compliance support</span></div>
        <div class="bc-line"><span class="tick">✓</span><span><strong>Quarterly</strong> cybersecurity awareness training</span></div>
        <div class="bc-line"><span class="tick">✓</span><span><strong>Phishing simulation</strong> for up to 50 users</span></div>
      </div>
    </div>
  </header>

  <!-- ─── TRUST STRIP ─── -->
  <div class="trust">
    <div class="wrap trust-inner">
      <div class="trust-item"><span class="n">2008</span><span class="l">Securing businesses since</span></div>
      <div class="trust-item"><span class="n">20+</span><span class="l">Years of combined expertise</span></div>
      <div class="trust-item"><span class="n">3</span><span class="l">Global offices</span></div>
      <div class="trust-iso">Certified: <b>ISO 27001</b> · <b>27701</b> · <b>22301</b></div>
    </div>
  </div>

  <!-- ─── WHAT'S INCLUDED ─── -->
  <section class="block">
    <div class="wrap">
      <div class="sec-head">
        <span class="eyebrow">What You Get</span>
        <h2>Five services, one engagement</h2>
        <p>Each piece closes a different gap. Together they give you continuous protection instead of a once-a-year checkbox.</p>
      </div>
      <div class="feat-grid">
        <div class="feat">
          <div class="ic">
            <svg viewBox="0 0 24 24"><path d="M12 2l8 3v6c0 5-3.5 8.5-8 11-4.5-2.5-8-6-8-11V5l8-3z"/><path d="M9 12l2 2 4-4"/></svg>
          </div>
          <h3>VAPT — Twice a Year</h3>
          <div class="spec">25 IP Addresses · 3 Web Apps</div>
          <p>Two full vulnerability assessment &amp; penetration testing cycles a year, so your systems are tested, not assumed safe.</p>
        </div>
        <div class="feat">
          <div class="ic">
            <svg viewBox="0 0 24 24"><path d="M12 3v4M12 17v4M3 12h4M17 12h4M5.6 5.6l2.8 2.8M15.6 15.6l2.8 2.8M18.4 5.6l-2.8 2.8M8.4 15.6l-2.8 2.8"/><circle cx="12" cy="12" r="3"/></svg>
          </div>
          <h3>VaptFix.ai Access</h3>
          <div class="spec">AI-Powered Remediation</div>
          <p>Turn findings into a prioritized action plan. Fix what actually matters first and track every issue to closure.</p>
        </div>
        <div class="feat">
          <div class="ic">
            <svg viewBox="0 0 24 24"><path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg>
          </div>
          <h3>ISO 27001 Support</h3>
          <div class="spec">Audit-Ready Guidance</div>
          <p>Get audit-ready and build client trust, guided by a team that is ISO 27001, 27701, and 22301 certified itself.</p>
        </div>
        <div class="feat">
          <div class="ic">
            <svg viewBox="0 0 24 24"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/></svg>
          </div>
          <h3>Quarterly Awareness Training</h3>
          <div class="spec">Every 3 Months</div>
          <p>Your people are your first line of defense. We keep your team sharp against the latest threats all year round.</p>
        </div>
        <div class="feat">
          <div class="ic">
            <svg viewBox="0 0 24 24"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
          </div>
          <h3>Phishing Simulation</h3>
          <div class="spec">Up to 50 Users</div>
          <p>Test how your team responds to a real-world phishing attempt — and turn risky clicks into teachable moments.</p>
        </div>
        <div class="feat">
          <div class="ic">
            <svg viewBox="0 0 24 24"><path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
          </div>
          <h3>One Partner, Not Five</h3>
          <div class="spec">End-to-End Coverage</div>
          <p>Stop juggling vendors. One contract, one team, one point of contact for your entire security posture.</p>
        </div>
      </div>
    </div>
  </section>

  <!-- ─── PROCESS ─── -->
  <section class="block alt">
    <div class="wrap">
      <div class="sec-head">
        <span class="eyebrow">How It Works</span>
        <h2>From enquiry to engagement</h2>
        <p>A straightforward path. Tell us about your environment and we'll get you a tailored quote.</p>
      </div>
      <div class="steps">
        <div class="step">
          <div class="num">1</div>
          <h4>Share your details</h4>
          <p>Fill in the short form below with your company and environment basics.</p>
        </div>
        <div class="step">
          <div class="num">2</div>
          <h4>Receive your quote</h4>
          <p>We scope the bundle to your needs and send pricing tailored to you.</p>
        </div>
        <div class="step">
          <div class="num">3</div>
          <h4>Kick-off call</h4>
          <p>A specialist walks you through scope, timelines, and onboarding.</p>
        </div>
        <div class="step">
          <div class="num">4</div>
          <h4>Year-round coverage</h4>
          <p>Testing, training, and compliance run on schedule — we handle the rest.</p>
        </div>
      </div>
    </div>
  </section>

  <!-- ─── LEAD FORM ─── -->
  <section class="block" id="quote">
    <div class="wrap quote-grid">
      <div class="quote-copy">
        <span class="eyebrow">Get Your Quote</span>
        <h2>Tell us about your <span>environment</span></h2>
        <p>Share a few details and we'll prepare a tailored quote. No obligation, no pressure.</p>
        <ul class="quote-assure">
          <li><span class="tick">✓</span> Tailored pricing within 1 business day</li>
          <li><span class="tick">✓</span> Reviewed by a security specialist</li>
          <li><span class="tick">✓</span> Your details are never shared or sold</li>
        </ul>
      </div>
      <form id="quoteForm" novalidate>
        <div class="form-intro">Fields marked <span style="color:var(--navy);font-weight:600;">*</span> are required. We'll use these only to prepare and send your quote.</div>
        <div class="form-row">
          <div class="field">
            <label for="fname">First Name <span class="req">*</span></label>
            <input type="text" id="fname" name="firstname" placeholder="Maria" required>
          </div>
          <div class="field">
            <label for="lname">Last Name <span class="req">*</span></label>
            <input type="text" id="lname" name="lastname" placeholder="Santos" required>
          </div>
        </div>
        <div class="field">
          <label for="company">Company <span class="req">*</span></label>
          <input type="text" id="company" name="company" placeholder="Your organization" required>
        </div>
        <div class="form-row">
          <div class="field">
            <label for="email">Work Email <span class="req">*</span></label>
            <input type="email" id="email" name="email" placeholder="you@company.com" required>
          </div>
          <div class="field">
            <label for="phone">Phone</label>
            <input type="tel" id="phone" name="phone" placeholder="+63 ___ ___ ____">
          </div>
        </div>
        <div class="form-row">
          <div class="field">
            <label for="size">Company Size</label>
            <select id="size" name="company_size">
              <option value="">Select…</option>
              <option value="1-50 Employees">1–50 employees</option>
              <option value="51-200 Employees">51–200 employees</option>
              <option value="201-1000 Employees">201–1000 employees</option>
              <option value="1000+ Employees">1000+ employees</option>
            </select>
          </div>
          <div class="field">
            <label for="timeline">Looking to start</label>
            <select id="timeline" name="looking_to_start">
              <option value="">Select…</option>
              <option value="Immediately">Immediately</option>
              <option value="Within 1 Month">Within 1 month</option>
              <option value="1-3 Months">1–3 months</option>
              <option value="Just Exploring">Just exploring</option>
            </select>
          </div>
        </div>
        <button type="submit" class="form-submit">Send My Quote Request →</button>
        <p id="formError" class="form-error" style="display:none;"></p>
        <p class="form-fine">By submitting, you agree to be contacted about your quote. See our <a href="https://secureitlab.com/privacy">privacy policy</a>.</p>
        <div class="form-success" id="formSuccess">
          <div class="check">
            <svg viewBox="0 0 24 24"><path d="M5 13l4 4L19 7"/></svg>
          </div>
          <h3>Request received</h3>
          <p>Your details are in. A specialist will prepare your tailored quote and be in touch within one business day.</p>
        </div>
      </form>
    </div>
  </section>

  <!-- ─── CLOSING CTA ─── -->
  <section class="closing">
    <div class="wrap closing-inner">
      <span class="eyebrow">Let's Get Started</span>
      <h2>Ready to <span>secure</span> your business?</h2>
      <p>One package. One partner. Complete peace of mind.</p>
      <a href="#quote"><button class="btn-prim">Get My Quote →</button></a>
    </div>
    <div class="yellow-bottom"></div>
  </section>

  <!-- ─── FOOTER ─── -->
  <footer>
    <div class="foot-main">
      <div class="foot-left">
        <img src="https://secureitlab.com/assets/images/secureitlab-logo.png" alt="SecureITLab">
        <div class="foot-contact-line">
          <strong>Email:</strong>&nbsp; <a href="mailto:info@secureitlab.com">info@secureitlab.com</a>
        </div>
        <div class="foot-contact-line" style="font-size:13px;color:rgba(13,46,94,0.7);margin-top:4px;">
          Remote-first cybersecurity &amp; data privacy consulting firm.
        </div>
      </div>
      <div class="foot-right">
        <p>SecureITLab is a remote-first cybersecurity, data privacy consulting &amp; solutions firm serving the industry since 2008. We firmly believe that security is a fundamental right for everyone. Our mission is to empower businesses of all sizes to navigate the complex realm of cybersecurity and data privacy with confidence and peace of mind.</p>
        <div class="foot-iso">
          <img src="https://secureitlab.com/assets/images/iso27001.png" alt="ISO 27001 Certified">
          <img src="https://secureitlab.com/assets/images/iso27701.png" alt="ISO 27701 Certified">
          <img src="https://secureitlab.com/assets/images/iso22301.png" alt="ISO 22301 Certified">
        </div>
      </div>
    </div>
    <div class="foot-bar">
      <div class="wrap foot-bar-inner">
        <span class="copy">© 2026 SecureITLab | All Rights Reserved</span>
        <div class="socials">
          <a href="#" aria-label="LinkedIn">
            <svg class="social-icon" viewBox="0 0 24 24"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"/><rect x="2" y="9" width="4" height="12"/><circle cx="4" cy="4" r="2"/></svg>
          </a>
          <a href="#" aria-label="Twitter / X">
            <svg class="social-icon" viewBox="0 0 24 24"><path d="M22 4s-.7 2.1-2 3.4c1.6 10-9.4 17.3-18 11.6 2.2.1 4.4-.6 6-2C3 15.5.5 9.6 3 5c2.2 2.6 5.6 4.1 9 4-.9-4.2 4-6.6 7-3.8 1.1 0 3-1.2 3-1.2z"/></svg>
          </a>
        </div>
        <a href="https://secureitlab.com/privacy" class="privacy">Privacy Policy</a>
      </div>
    </div>
  </footer>
</template>

<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --navy:       #1B4080;
  --navy-dark:  #0D2E5E;
  --navy-deep:  #0A2347;
  --yellow:     #F5C400;
  --yellow-dk:  #D4A900;
  --yellow-lt:  #FEF9E0;
  --bg:         #FFFFFF;
  --surface:    #F7F9FB;
  --body:       #374151;
  --muted:      #6B7280;
  --light:      #9CA3AF;
  --border:     #E5E7EB;
  --border2:    #D1D5DB;
  --shadow-sm:  0 1px 4px rgba(0,0,0,.07), 0 1px 2px rgba(0,0,0,.04);
  --shadow-md:  0 4px 18px rgba(0,0,0,.09), 0 2px 6px rgba(0,0,0,.05);
  --font-h:     'Montserrat', sans-serif;
  --font-b:     'Inter', sans-serif;
}

html { font-size: 16px; scroll-behavior: smooth; }
body {
  background: var(--bg);
  color: var(--body);
  font-family: var(--font-b);
  line-height: 1.65;
  -webkit-font-smoothing: antialiased;
  overflow-x: hidden;
}

a { color: inherit; text-decoration: none; }
::selection { background: var(--yellow); color: var(--navy-dark); }

.wrap { max-width: 1160px; margin: 0 auto; padding: 0 32px; }

/* ─── NAV ─── */
nav {
  position: sticky;
  top: 0;
  z-index: 50;
  background: rgba(255,255,255,0.97);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid var(--border);
  box-shadow: var(--shadow-sm);
}
.nav-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 70px;
}
.nav-logo { display: flex; align-items: center; }
.nav-logo img { height: 38px; width: auto; display: block; }

.nav-cta {
  font-family: var(--font-h);
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.03em;
  padding: 11px 26px;
  background: var(--yellow);
  color: var(--navy-dark);
  border-radius: 50px;
  transition: background 0.2s;
  white-space: nowrap;
}
.nav-cta:hover { background: var(--yellow-dk); }

/* ─── HERO ─── */
.hero {
  background: var(--surface);
  border-bottom: 1px solid var(--border);
  padding: 52px 0 64px;
  position: relative;
  overflow: hidden;
}
.hero::before {
  content: '';
  position: absolute;
  top: -80px; right: -80px;
  width: 480px; height: 480px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(245,196,0,0.09) 0%, transparent 68%);
  pointer-events: none;
}
.hero-grid {
  position: relative;
  z-index: 2;
  display: grid;
  grid-template-columns: 1.1fr 0.9fr;
  gap: 56px;
  align-items: center;
}
.eyebrow {
  display: inline-block;
  font-family: var(--font-h);
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--navy);
  background: rgba(27,64,128,0.07);
  padding: 5px 14px;
  border-radius: 50px;
  margin-bottom: 18px;
}
.hero h1 {
  font-family: var(--font-h);
  font-size: clamp(34px, 4.6vw, 54px);
  font-weight: 800;
  line-height: 1.08;
  letter-spacing: -0.02em;
  color: var(--navy-dark);
  margin-bottom: 20px;
}
.hero h1 .accent { color: var(--navy); }
.hero .lede {
  font-size: 17px;
  color: var(--muted);
  max-width: 500px;
  margin-bottom: 24px;
  line-height: 1.7;
}

.hero-stats {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 32px;
  padding: 14px 20px;
  background: #fff;
  border: 1px solid var(--border);
  border-radius: 10px;
  width: fit-content;
  box-shadow: var(--shadow-sm);
}
.hstat { display: flex; flex-direction: column; gap: 2px; }
.hstat-n { font-family: var(--font-h); font-size: 22px; font-weight: 800; color: var(--navy); line-height: 1; }
.hstat-l { font-size: 11px; color: var(--muted); white-space: nowrap; }
.hstat-div { width: 1px; height: 32px; background: var(--border2); flex-shrink: 0; }

.hero-actions { display: flex; gap: 14px; flex-wrap: wrap; align-items: center; }
.hero-note { font-size: 12.5px; color: var(--light); }

.btn-prim {
  font-family: var(--font-h);
  font-size: 14px;
  font-weight: 700;
  letter-spacing: 0.03em;
  padding: 14px 32px;
  background: var(--yellow);
  color: var(--navy-dark);
  border: none;
  border-radius: 50px;
  cursor: pointer;
  transition: background 0.2s, transform 0.1s;
  box-shadow: 0 4px 14px rgba(245,196,0,0.35);
}
.btn-prim:hover { background: var(--yellow-dk); }
.btn-prim:active { transform: translateY(1px); }

.bundle-card {
  background: var(--bg);
  border: 1px solid var(--border2);
  border-radius: 12px;
  box-shadow: var(--shadow-md);
  overflow: hidden;
}
.bc-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 18px 24px;
  background: var(--navy);
}
.bc-title { font-family: var(--font-h); font-size: 13px; font-weight: 700; color: #fff; }
.bc-tag {
  font-family: var(--font-h); font-size: 10px; font-weight: 700; letter-spacing: 0.08em;
  color: var(--navy-dark); background: var(--yellow);
  padding: 3px 10px; border-radius: 20px;
}
.bc-line {
  display: flex; gap: 12px; align-items: flex-start;
  padding: 13px 24px; border-bottom: 1px solid var(--border);
  font-size: 14px; color: var(--body);
}
.bc-line:last-child { border-bottom: none; }
.bc-line .tick { color: var(--navy); font-size: 15px; font-weight: 700; flex-shrink: 0; margin-top: 2px; }
.vaptfix-link { color: var(--navy); text-decoration: none; font-weight: 700; }
.vaptfix-link:hover { color: var(--navy-dark); }

/* ─── TRUST STRIP ─── */
.trust { background: var(--navy); padding: 26px 0; }
.trust-inner {
  display: flex; flex-wrap: wrap;
  align-items: center; justify-content: space-between; gap: 24px;
}
.trust-item { display: flex; align-items: center; gap: 10px; }
.trust-item .n { font-family: var(--font-h); font-size: 28px; font-weight: 800; color: var(--yellow); line-height: 1; }
.trust-item .l { font-size: 13px; color: rgba(255,255,255,0.6); max-width: 140px; line-height: 1.3; }
.trust-iso { font-size: 12px; color: rgba(255,255,255,0.5); letter-spacing: 0.04em; }
.trust-iso b { color: rgba(255,255,255,0.85); font-weight: 600; }

/* ─── SECTIONS ─── */
section.block { padding: 80px 0; border-bottom: 1px solid var(--border); }
section.block.alt { background: var(--surface); }
.sec-head { margin-bottom: 48px; max-width: 580px; }
.sec-head .eyebrow { margin-bottom: 14px; }
.sec-head h2 {
  font-family: var(--font-h);
  font-size: clamp(26px, 3.2vw, 34px);
  font-weight: 700; color: var(--navy-dark);
  letter-spacing: -0.015em; line-height: 1.18; margin-bottom: 12px;
}
.sec-head p { font-size: 16px; color: var(--muted); }

/* ─── FEATURE CARDS ─── */
.feat-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 20px; }
.feat {
  background: var(--bg); border: 1px solid var(--border); border-radius: 10px;
  padding: 28px 26px; box-shadow: var(--shadow-sm);
  border-top: 3px solid var(--navy);
  transition: box-shadow 0.2s, transform 0.2s;
}
.feat:hover { box-shadow: var(--shadow-md); transform: translateY(-3px); }
.feat:last-child { border-top-color: var(--navy); }
.feat .ic {
  width: 46px; height: 46px;
  background: rgba(27,64,128,0.08); border-radius: 8px;
  display: flex; align-items: center; justify-content: center; margin-bottom: 18px;
}
.feat .ic svg { width: 22px; height: 22px; stroke: var(--navy); fill: none; stroke-width: 1.8; }
.feat h3 { font-family: var(--font-h); font-size: 16px; font-weight: 700; color: var(--navy-dark); margin-bottom: 6px; }
.feat .spec {
  font-family: var(--font-h); font-size: 10.5px; font-weight: 700;
  color: var(--navy); letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 10px;
}
.feat p { font-size: 13.5px; color: var(--muted); line-height: 1.6; }

/* ─── PROCESS ─── */
.steps { display: grid; grid-template-columns: repeat(4,1fr); gap: 0; }
.step { position: relative; padding: 0 24px 0 0; }
.step:not(:last-child)::after {
  content: ''; position: absolute;
  top: 12px; right: calc(50% - 26px);
  width: 14px; height: 14px;
  border-top: 2px solid var(--border2);
  border-right: 2px solid var(--border2);
  transform: rotate(45deg);
}
.step .num {
  font-family: var(--font-h); font-size: 13px; font-weight: 800;
  color: var(--navy-dark); background: var(--yellow);
  width: 38px; height: 38px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  margin-bottom: 18px; box-shadow: 0 4px 10px rgba(245,196,0,0.35);
}
.step h4 { font-family: var(--font-h); font-size: 15px; font-weight: 700; color: var(--navy-dark); margin-bottom: 7px; }
.step p { font-size: 13.5px; color: var(--muted); line-height: 1.55; }

/* ─── QUOTE FORM ─── */
.quote-grid { display: grid; grid-template-columns: 0.95fr 1.05fr; gap: 56px; align-items: start; }
.quote-copy .eyebrow { margin-bottom: 14px; }
.quote-copy h2 {
  font-family: var(--font-h); font-size: clamp(26px, 3.4vw, 36px);
  font-weight: 800; color: var(--navy-dark); line-height: 1.15;
  letter-spacing: -0.015em; margin-bottom: 16px;
}
.quote-copy h2 span { color: var(--navy); }
.quote-copy p { font-size: 15px; color: var(--muted); margin-bottom: 28px; max-width: 380px; }
.quote-assure { list-style: none; }
.quote-assure li {
  display: flex; gap: 12px; font-size: 14px; color: var(--body);
  padding: 11px 0; border-bottom: 1px solid var(--border); line-height: 1.45;
}
.quote-assure li:last-child { border-bottom: none; }
.quote-assure .tick { color: var(--navy); font-weight: 700; font-size: 16px; flex-shrink: 0; }

form {
  background: var(--bg); border: 1px solid var(--border);
  border-radius: 12px; padding: 36px; box-shadow: var(--shadow-md);
}
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.field { margin-bottom: 18px; }
label {
  display: block; font-family: var(--font-h); font-size: 11px; font-weight: 700;
  letter-spacing: 0.1em; text-transform: uppercase; color: var(--muted); margin-bottom: 7px;
}
label .req { color: var(--navy); }
input, select {
  width: 100%; background: var(--surface); border: 1.5px solid var(--border2);
  border-radius: 6px; padding: 11px 14px; color: var(--navy-dark);
  font-family: var(--font-b); font-size: 14px;
  transition: border-color 0.18s, box-shadow 0.18s;
}
input::placeholder { color: var(--light); }
input:focus, select:focus {
  outline: none; border-color: var(--navy);
  box-shadow: 0 0 0 3px rgba(27,64,128,0.1); background: #fff;
}
select {
  appearance: none; cursor: pointer;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath d='M2 4l4 4 4-4' stroke='%231B4080' stroke-width='1.5' fill='none'/%3E%3C/svg%3E");
  background-repeat: no-repeat; background-position: right 14px center;
  background-color: var(--surface);
}
.form-submit {
  width: 100%; font-family: var(--font-h); font-size: 14px; font-weight: 700;
  letter-spacing: 0.03em; padding: 15px; background: var(--yellow); color: var(--navy-dark);
  border: none; border-radius: 50px; cursor: pointer; margin-top: 6px;
  transition: background 0.2s, transform 0.1s;
  box-shadow: 0 4px 14px rgba(245,196,0,0.35);
}
.form-submit:hover { background: var(--yellow-dk); }
.form-submit:active { transform: translateY(1px); }
.form-fine { font-size: 11.5px; color: var(--light); text-align: center; margin-top: 14px; line-height: 1.5; }
.form-error { font-size: 13px; color: #DC2626; text-align: center; margin-top: 12px; padding: 10px 14px; background: #FEF2F2; border: 1px solid #FECACA; border-radius: 6px; }
.form-fine a { color: var(--muted); text-decoration: underline; }
.form-intro { font-size: 13px; color: var(--muted); margin-bottom: 24px; padding-bottom: 20px; border-bottom: 1px solid var(--border); }

.form-success { display: none; text-align: center; padding: 24px 8px; }
.form-success.show { display: block; }
.form-success .check {
  width: 60px; height: 60px; margin: 0 auto 20px; border-radius: 50%;
  background: rgba(27,64,128,0.08); border: 2px solid rgba(27,64,128,0.25);
  display: flex; align-items: center; justify-content: center;
}
.form-success .check svg { width: 26px; height: 26px; stroke: var(--navy); fill: none; stroke-width: 2.4; }
.form-success h3 { font-family: var(--font-h); font-size: 20px; font-weight: 700; color: var(--navy-dark); margin-bottom: 10px; }
.form-success p { font-size: 14px; color: var(--muted); max-width: 320px; margin: 0 auto; }
form.sent .field,
form.sent .form-row,
form.sent .form-submit,
form.sent .form-fine,
form.sent .form-intro { display: none; }

/* ─── CLOSING CTA ─── */
.closing { background: var(--navy); text-align: center; padding: 88px 0; position: relative; overflow: hidden; }
.closing::before {
  content: ''; position: absolute; top: 50%; left: 50%;
  transform: translate(-50%,-50%); width: 600px; height: 600px;
  border-radius: 50%; border: 1px solid rgba(255,255,255,0.05); pointer-events: none;
}
.closing::after {
  content: ''; position: absolute; top: 50%; left: 50%;
  transform: translate(-50%,-50%); width: 400px; height: 400px;
  border-radius: 50%; border: 1px solid rgba(255,255,255,0.07); pointer-events: none;
}
.closing-inner { position: relative; z-index: 2; }
.closing .eyebrow { background: rgba(255,255,255,0.1); color: var(--yellow); margin-bottom: 18px; }
.closing h2 {
  font-family: var(--font-h); font-size: clamp(28px,4.2vw,46px); font-weight: 800;
  color: #fff; line-height: 1.1; letter-spacing: -0.02em; margin-bottom: 16px;
}
.closing h2 span { color: var(--yellow); }
.closing p { font-size: 16px; color: rgba(255,255,255,0.55); margin-bottom: 34px; }
.yellow-bottom { position: absolute; bottom: 0; left: 0; width: 100%; height: 4px; background: var(--yellow); }

/* ─── FOOTER ─── */
.foot-main { display: grid; grid-template-columns: 1fr 1fr; }
.foot-left {
  background: var(--yellow);
  padding: 44px 48px;
  display: flex; flex-direction: column; gap: 16px;
}
.foot-left img { height: 24px; width: auto; max-width: 175px; margin-bottom: 4px; }
.foot-left .foot-contact-line { font-size: 14px; color: var(--navy-dark); line-height: 1.6; }
.foot-left .foot-contact-line a { color: var(--navy-dark); font-weight: 600; }
.foot-left .foot-contact-line a:hover { text-decoration: underline; }
.foot-right {
  background: var(--navy);
  padding: 44px 48px;
  display: flex; flex-direction: column; justify-content: space-between; gap: 24px;
}
.foot-right p { font-size: 13.5px; color: rgba(255,255,255,0.7); line-height: 1.7; }
.foot-iso { display: flex; align-items: center; gap: 16px; margin-top: 8px; }
.foot-iso img { height: 64px; width: auto; filter: brightness(0) invert(1); opacity: 0.85; }
.foot-bar { background: var(--bg); border-top: 1px solid var(--border); padding: 18px 0; }
.foot-bar-inner {
  display: flex; align-items: center; justify-content: space-between;
  flex-wrap: wrap; gap: 12px;
}
.foot-bar .copy { font-size: 13px; color: var(--muted); }
.foot-bar .socials { display: flex; gap: 16px; align-items: center; }
.foot-bar .socials a { color: var(--muted); font-size: 13px; transition: color 0.2s; }
.foot-bar .socials a:hover { color: var(--navy); }
.foot-bar .privacy { font-size: 13px; color: var(--muted); }
.foot-bar .privacy:hover { color: var(--navy); text-decoration: underline; }

.social-icon { width: 18px; height: 18px; fill: currentColor; display: block; }

/* ─── RESPONSIVE ─── */
@media (max-width: 900px) {
  .hero { padding: 40px 0 52px; }
  .hero .lede { font-size: 16px; }
  .hero-grid { grid-template-columns: 1fr; gap: 36px; }
  section.block { padding: 60px 0; }
  .closing { padding: 64px 0; }
  .quote-grid { grid-template-columns: 1fr; gap: 32px; }
  .steps { grid-template-columns: 1fr 1fr; }
  .step:nth-child(2)::after { display: none; }
  .trust-inner { justify-content: center; gap: 16px; }
  .foot-main { grid-template-columns: 1fr; }
  .foot-left, .foot-right { padding: 36px 32px; }
}
@media (max-width: 560px) {
  .wrap { padding: 0 20px; }
  .nav-logo img { height: 32px; }
  .nav-cta { font-size: 12px; padding: 9px 18px; }
  .hero { padding: 28px 0 36px; }
  .hero .lede { font-size: 15px; }
  .hero-actions { gap: 10px; }
  .hero-stats { flex-wrap: wrap; gap: 12px; width: 100%; padding: 12px 16px; }
  .hstat-div { display: none; }
  .hstat { flex-direction: row; align-items: center; gap: 6px; }
  .hstat-n { font-size: 18px; }
  section.block { padding: 44px 0; }
  .sec-head { margin-bottom: 32px; }
  .closing { padding: 44px 0; }
  .trust { padding: 18px 0; }
  .trust-inner { flex-direction: column; align-items: center; text-align: center; gap: 14px; }
  .trust-item { flex-direction: column; align-items: center; gap: 4px; }
  .trust-item .n { font-size: 24px; }
  .trust-item .l { text-align: center; max-width: none; }
  .trust-iso { text-align: center; }
  .form-row { grid-template-columns: 1fr; }
  .steps { grid-template-columns: 1fr; }
  .step::after { display: none !important; }
  form { padding: 24px 20px; }
  .foot-left, .foot-right { padding: 28px 20px; }
  .foot-iso { flex-wrap: wrap; gap: 12px; }
  .foot-iso img { height: 48px; }
  .foot-bar-inner { flex-direction: column; align-items: center; text-align: center; gap: 8px; }
  .quote-copy p { max-width: 100%; }
}

@keyframes rise { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: none; } }
.reveal    { animation: rise 0.55s ease both; }
.reveal.d1 { animation-delay: 0.05s; }
.reveal.d2 { animation-delay: 0.14s; }
.reveal.d3 { animation-delay: 0.23s; }
@media (prefers-reduced-motion: reduce) {
  .reveal { animation: none; }
  * { transition: none !important; scroll-behavior: auto !important; }
}
</style>
