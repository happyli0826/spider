// var main_url = "aHR0cDovL3YzLWRlZmF1bHQuaXhpZ3VhLmNvbS80OTI2OGEzOGMxYzRkNzcxMjQ0MDA4OWE1Yjk0MmQ5Yy81Y2E0OWE1Ni92aWRlby9tLzIyMDU3ODMwMzAwNmI2ODQxZjI5ZGM1Zjc5ZGYwNTc2ODE4MTE1OTU2YTQwMDAwNjJjOTViZjVlMTYxLz9yYz1NM2h4YkdocGNEVnlaek16T2pjek0wQXBRSFJBYnpRMk9EUTdNek16TXpnMk5ETXpORFZ2UUdnemRTbEFaak4xS1dSemNtZDVhM1Z5WjNseWJIaDNaamMyUUdKaU16Vm1OR0JqTlY4dExXSXRMM056TFc4amJ5TTJMelF2TWpVdExqWXVOVEF4TmkwNkkyOGpPbUV0Y1NNNllIWnBYR0ptSzJCZVltWXJYbkZzT2lNekxsNCUzRA=="
// main_url  = new Buffer.from(main_url, 'base64').toString();
// // var a = main_url.replace(/^http:/, "");
// var a = main_url
// a = a.indexOf("?") > 0 ? a + "&vfrom=xgplayer" : a + "?vfrom=xgplayer";
//
// console.log(a);

const jsdom = require("jsdom");
const {JSDOM} = jsdom;
const dom = new JSDOM("<!DOCTYPE html><p>Hello world</p>");
window = dom.window;
document = window.document;
location = window.location;

e = {};

var a = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function(t) {
        return typeof t
    }
    : function(t) {
        return t && "function" == typeof Symbol && t.constructor === Symbol && t !== Symbol.prototype ? "symbol" : typeof t
    };

function i(t) {
    var c = /^([a-z][a-z0-9.+-]*:)?(\/\/)?([\S\s]*)/i;
    var e = c.exec(t);
    return {
        protocol: e[1] ? e[1].toLowerCase() : "",
        slashes: !!e[2],
        rest: e[3]
    }
}

s = function(t, e) {
    if (e = e.split(":")[0],
        !(t = +t))
        return !1;
    switch (e) {
        case "http":
        case "ws":
            return 80 !== t;
        case "https":
        case "wss":
            return 443 !== t;
        case "ftp":
            return 21 !== t;
        case "gopher":
            return 70 !== t;
        case "file":
            return !1
    }
    return 0 !== t
};

function r(t) {
    var l = /^[A-Za-z][A-Za-z0-9+-.]*:\/\//;
    var n, r = {}, i = void 0 === (t = t || e.location || {}) ? "undefined" : a(t);
    if ("blob:" === t.protocol)
        r = new o(unescape(t.pathname),{});
    else if ("string" === i)
        for (n in r = new o(t,{}),
            p)
            delete r[n];
    else if ("object" === i) {
        for (n in t)
            n in p || (r[n] = t[n]);
        void 0 === r.slashes && (r.slashes = l.test(t.href))
    }
    return false
}
function o(t, e, n) {
    if (!(this instanceof o))
        return new o(t,e,n);
    var f = [["#", "hash"], ["?", "query"], ["/", "pathname"], ["@", "auth", 1], [NaN, "host", void 0, 1, 1], [/:(\d+)$/, "port", void 0, 1], [NaN, "hostname", void 0, 1, 1]];
    var c, l, p, d, h, v, g = f.slice(), y = void 0 === e ? "undefined" : a(e), m = this, b = 0;
    for ("object" !== y && "string" !== y && (n = e,
        e = null),
         n && "function" != typeof n && (n = u.parse),
             e = r(e),
             c = !(l = i(t || "")).protocol && !l.slashes,
             m.slashes = l.slashes || c && e.slashes,
             m.protocol = l.protocol || e.protocol || "",
             t = l.rest,
         l.slashes || (g[2] = [/(.*)/, "pathname"]); b < g.length; b++)
        p = (d = g[b])[0],
            v = d[1],
            p != p ? m[v] = t : "string" == typeof p ? ~(h = t.indexOf(p)) && ("number" == typeof d[2] ? (m[v] = t.slice(0, h),
                t = t.slice(h + d[2])) : (m[v] = t.slice(h),
                t = t.slice(0, h))) : (h = p.exec(t)) && (m[v] = h[1],
                t = t.slice(0, h.index)),
            m[v] = m[v] || c && d[3] && e[v] || "",
        d[4] && (m[v] = m[v].toLowerCase());
    n && (m.query = n(m.query)),
    c && e.slashes && "/" !== m.pathname.charAt(0) && ("" !== m.pathname || "" !== e.pathname) && (m.pathname = function(t, e) {
        for (var n = (e || "/").split("/").slice(0, -1).concat(t.split("/")), r = n.length, i = n[r - 1], o = !1, a = 0; r--; )
            "." === n[r] ? n.splice(r, 1) : ".." === n[r] ? (n.splice(r, 1),
                a++) : a && (0 === r && (o = !0),
                n.splice(r, 1),
                a--);
        return o && n.unshift(""),
        "." !== i && ".." !== i || n.push(""),
            n.join("/")
    }(m.pathname, e.pathname)),
    s(m.port, m.protocol) || (m.host = m.hostname,
        m.port = ""),
        m.username = m.password = "",
    m.auth && (d = m.auth.split(":"),
        m.username = d[0] || "",
        m.password = d[1] || ""),
        m.origin = m.protocol && m.host && "file:" !== m.protocol ? m.protocol + "//" + m.host : "null",
        m.href = m.toString()
}
b_fun = function(t) {
    var e;
    document ? e = new o(t) : (document.createElement("a"),
        e.href = t);
    var n = function() {
        for (var t = 0, e = new Array(256), n = 0; 256 !== n; ++n)
            t = 1 & (t = 1 & (t = 1 & (t = 1 & (t = 1 & (t = 1 & (t = 1 & (t = 1 & (t = n) ? -306674912 ^ t >>> 1 : t >>> 1) ? -306674912 ^ t >>> 1 : t >>> 1) ? -306674912 ^ t >>> 1 : t >>> 1) ? -306674912 ^ t >>> 1 : t >>> 1) ? -306674912 ^ t >>> 1 : t >>> 1) ? -306674912 ^ t >>> 1 : t >>> 1) ? -306674912 ^ t >>> 1 : t >>> 1) ? -306674912 ^ t >>> 1 : t >>> 1,
                e[n] = t;
        return "undefined" != typeof Int32Array ? new Int32Array(e) : e
    }()
        , r = e.pathname + "?r=" + Math.random().toString(10).substring(2);
    "/" !== r[0] && (r = "/" + r);
    var i = function(t) {
        for (var e, r, i = -1, o = 0, a = t.length; o < a; )
            (e = t.charCodeAt(o++)) < 128 ? i = i >>> 8 ^ n[255 & (i ^ e)] : e < 2048 ? i = (i = i >>> 8 ^ n[255 & (i ^ (192 | e >> 6 & 31))]) >>> 8 ^ n[255 & (i ^ (128 | 63 & e))] : e >= 55296 && e < 57344 ? (e = 64 + (1023 & e),
                r = 1023 & t.charCodeAt(o++),
                i = (i = (i = (i = i >>> 8 ^ n[255 & (i ^ (240 | e >> 8 & 7))]) >>> 8 ^ n[255 & (i ^ (128 | e >> 2 & 63))]) >>> 8 ^ n[255 & (i ^ (128 | r >> 6 & 15 | (3 & e) << 4))]) >>> 8 ^ n[255 & (i ^ (128 | 63 & r))]) : i = (i = (i = i >>> 8 ^ n[255 & (i ^ (224 | e >> 12 & 15))]) >>> 8 ^ n[255 & (i ^ (128 | e >> 6 & 63))]) >>> 8 ^ n[255 & (i ^ (128 | 63 & e))];
        return -1 ^ i
    }(r) >>> 0;
    return (document && location.protocol.indexOf("http") > -1 ? [location.protocol, e.hostname] : ["http:", e.hostname]).join("//") + r + "&s=" + i
};
function get_video_url (t) {
    var e = arguments.length > 1 && void 0 !== arguments[1] ? arguments[1] : "//ib.365yg.com/video/urls/v/1/toutiao/mp4/"
        , n = arguments.length > 2 && void 0 !== arguments[2] ? arguments[2] : {}
        , r = arguments.length > 3 && void 0 !== arguments[3] ? arguments[3] : {};
    if (t) {
        var url = (0, b_fun)(e + t);
        console.log(url);
        return url

    }
}

// get_video_url('v02004e70000bd8of2cm7fie8i6neue0');


