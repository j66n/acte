(function(){const t=document.createElement("link").relList;if(t&&t.supports&&t.supports("modulepreload"))return;for(const r of document.querySelectorAll('link[rel="modulepreload"]'))n(r);new MutationObserver(r=>{for(const l of r)if(l.type==="childList")for(const i of l.addedNodes)i.tagName==="LINK"&&i.rel==="modulepreload"&&n(i)}).observe(document,{childList:!0,subtree:!0});function s(r){const l={};return r.integrity&&(l.integrity=r.integrity),r.referrerPolicy&&(l.referrerPolicy=r.referrerPolicy),r.crossOrigin==="use-credentials"?l.credentials="include":r.crossOrigin==="anonymous"?l.credentials="omit":l.credentials="same-origin",l}function n(r){if(r.ep)return;r.ep=!0;const l=s(r);fetch(r.href,l)}})();const ye=(e,t)=>e===t,_e=Symbol("solid-track"),R={equals:ye};let ae=de;const O=1,H=2,ce={owned:null,cleanups:null,context:null,owner:null};var v=null;let Z=null,ve=null,_=null,S=null,T=null,Q=0;function J(e,t){const s=_,n=v,r=e.length===0,l=t===void 0?n:t,i=r?ce:{owned:null,cleanups:null,context:l?l.context:null,owner:l},o=r?e:()=>e(()=>E(()=>W(i)));v=i,_=null;try{return L(o,!0)}finally{_=s,v=n}}function P(e,t){t=t?Object.assign({},R,t):R;const s={value:e,observers:null,observerSlots:null,comparator:t.equals||void 0},n=r=>(typeof r=="function"&&(r=r(s.value)),fe(s,r));return[ue.bind(s),n]}function D(e,t,s){const n=se(e,t,!1,O);U(n)}function me(e,t,s){ae=ke;const n=se(e,t,!1,O);n.user=!0,T?T.push(n):U(n)}function k(e,t,s){s=s?Object.assign({},R,s):R;const n=se(e,t,!0,0);return n.observers=null,n.observerSlots=null,n.comparator=s.equals||void 0,U(n),ue.bind(n)}function E(e){if(_===null)return e();const t=_;_=null;try{return e()}finally{_=t}}function $e(e){return v===null||(v.cleanups===null?v.cleanups=[e]:v.cleanups.push(e)),e}function Se(e){const t=k(e),s=k(()=>z(t()));return s.toArray=()=>{const n=s();return Array.isArray(n)?n:n!=null?[n]:[]},s}function ue(){if(this.sources&&this.state)if(this.state===O)U(this);else{const e=S;S=null,L(()=>K(this),!1),S=e}if(_){const e=this.observers?this.observers.length:0;_.sources?(_.sources.push(this),_.sourceSlots.push(e)):(_.sources=[this],_.sourceSlots=[e]),this.observers?(this.observers.push(_),this.observerSlots.push(_.sources.length-1)):(this.observers=[_],this.observerSlots=[_.sources.length-1])}return this.value}function fe(e,t,s){let n=e.value;return(!e.comparator||!e.comparator(n,t))&&(e.value=t,e.observers&&e.observers.length&&L(()=>{for(let r=0;r<e.observers.length;r+=1){const l=e.observers[r],i=Z&&Z.running;i&&Z.disposed.has(l),(i?!l.tState:!l.state)&&(l.pure?S.push(l):T.push(l),l.observers&&he(l)),i||(l.state=O)}if(S.length>1e6)throw S=[],new Error},!1)),t}function U(e){if(!e.fn)return;W(e);const t=Q;Ce(e,e.value,t)}function Ce(e,t,s){let n;const r=v,l=_;_=v=e;try{n=e.fn(t)}catch(i){return e.pure&&(e.state=O,e.owned&&e.owned.forEach(W),e.owned=null),e.updatedAt=s+1,ge(i)}finally{_=l,v=r}(!e.updatedAt||e.updatedAt<=s)&&(e.updatedAt!=null&&"observers"in e?fe(e,n):e.value=n,e.updatedAt=s)}function se(e,t,s,n=O,r){const l={fn:e,state:n,updatedAt:null,owned:null,sources:null,sourceSlots:null,cleanups:null,value:t,owner:v,context:v?v.context:null,pure:s};return v===null||v!==ce&&(v.owned?v.owned.push(l):v.owned=[l]),l}function F(e){if(e.state===0)return;if(e.state===H)return K(e);if(e.suspense&&E(e.suspense.inFallback))return e.suspense.effects.push(e);const t=[e];for(;(e=e.owner)&&(!e.updatedAt||e.updatedAt<Q);)e.state&&t.push(e);for(let s=t.length-1;s>=0;s--)if(e=t[s],e.state===O)U(e);else if(e.state===H){const n=S;S=null,L(()=>K(e,t[0]),!1),S=n}}function L(e,t){if(S)return e();let s=!1;t||(S=[]),T?s=!0:T=[],Q++;try{const n=e();return Ae(s),n}catch(n){s||(T=null),S=null,ge(n)}}function Ae(e){if(S&&(de(S),S=null),e)return;const t=T;T=null,t.length&&L(()=>ae(t),!1)}function de(e){for(let t=0;t<e.length;t++)F(e[t])}function ke(e){let t,s=0;for(t=0;t<e.length;t++){const n=e[t];n.user?e[s++]=n:F(n)}for(t=0;t<s;t++)F(e[t])}function K(e,t){e.state=0;for(let s=0;s<e.sources.length;s+=1){const n=e.sources[s];if(n.sources){const r=n.state;r===O?n!==t&&(!n.updatedAt||n.updatedAt<Q)&&F(n):r===H&&K(n,t)}}}function he(e){for(let t=0;t<e.observers.length;t+=1){const s=e.observers[t];s.state||(s.state=H,s.pure?S.push(s):T.push(s),s.observers&&he(s))}}function W(e){let t;if(e.sources)for(;e.sources.length;){const s=e.sources.pop(),n=e.sourceSlots.pop(),r=s.observers;if(r&&r.length){const l=r.pop(),i=s.observerSlots.pop();n<r.length&&(l.sourceSlots[i]=n,r[n]=l,s.observerSlots[n]=i)}}if(e.owned){for(t=e.owned.length-1;t>=0;t--)W(e.owned[t]);e.owned=null}if(e.cleanups){for(t=e.cleanups.length-1;t>=0;t--)e.cleanups[t]();e.cleanups=null}e.state=0}function Me(e){return e instanceof Error?e:new Error(typeof e=="string"?e:"Unknown error",{cause:e})}function ge(e,t=v){throw Me(e)}function z(e){if(typeof e=="function"&&!e.length)return z(e());if(Array.isArray(e)){const t=[];for(let s=0;s<e.length;s++){const n=z(e[s]);Array.isArray(n)?t.push.apply(t,n):t.push(n)}return t}return e}const Ie=Symbol("fallback");function le(e){for(let t=0;t<e.length;t++)e[t]()}function Te(e,t,s={}){let n=[],r=[],l=[],i=0,o=t.length>1?[]:null;return $e(()=>le(l)),()=>{let f=e()||[],c=f.length,u,a;return f[_e],E(()=>{let w,m,x,C,y,g,p,$,M;if(c===0)i!==0&&(le(l),l=[],n=[],r=[],i=0,o&&(o=[])),s.fallback&&(n=[Ie],r[0]=J(V=>(l[0]=V,s.fallback())),i=1);else if(i===0){for(r=new Array(c),a=0;a<c;a++)n[a]=f[a],r[a]=J(d);i=c}else{for(x=new Array(c),C=new Array(c),o&&(y=new Array(c)),g=0,p=Math.min(i,c);g<p&&n[g]===f[g];g++);for(p=i-1,$=c-1;p>=g&&$>=g&&n[p]===f[$];p--,$--)x[$]=r[p],C[$]=l[p],o&&(y[$]=o[p]);for(w=new Map,m=new Array($+1),a=$;a>=g;a--)M=f[a],u=w.get(M),m[a]=u===void 0?-1:u,w.set(M,a);for(u=g;u<=p;u++)M=n[u],a=w.get(M),a!==void 0&&a!==-1?(x[a]=r[u],C[a]=l[u],o&&(y[a]=o[u]),a=m[a],w.set(M,a)):l[u]();for(a=g;a<c;a++)a in x?(r[a]=x[a],l[a]=C[a],o&&(o[a]=y[a],o[a](a))):r[a]=J(d);r=r.slice(0,i=c),n=f.slice(0)}return r});function d(w){if(l[a]=w,o){const[m,x]=P(a);return o[a]=x,t(f[a],m)}return t(f[a])}}}let Ee=!1;function A(e,t){return E(()=>e(t||{}))}const pe=e=>`Stale read from <${e}>.`;function be(e){const t="fallback"in e&&{fallback:()=>e.fallback};return k(Te(()=>e.each,e.children,t||void 0))}function j(e){const t=e.keyed,s=k(()=>e.when,void 0,{equals:(n,r)=>t?n===r:!n==!r});return k(()=>{const n=s();if(n){const r=e.children;return typeof r=="function"&&r.length>0?E(()=>r(t?n:()=>{if(!E(s))throw pe("Show");return e.when})):r}return e.fallback},void 0,void 0)}function Oe(e){let t=!1;const s=(l,i)=>(t?l[1]===i[1]:!l[1]==!i[1])&&l[2]===i[2],n=Se(()=>e.children),r=k(()=>{let l=n();Array.isArray(l)||(l=[l]);for(let i=0;i<l.length;i++){const o=l[i].when;if(o)return t=!!l[i].keyed,[i,o,l[i]]}return[-1]},void 0,{equals:s});return k(()=>{const[l,i,o]=r();if(l<0)return e.fallback;const f=o.children;return typeof f=="function"&&f.length>0?E(()=>f(t?i:()=>{if(E(r)[0]!==l)throw pe("Match");return o.when})):f},void 0,void 0)}function re(e){return e}function De(e,t,s){let n=s.length,r=t.length,l=n,i=0,o=0,f=t[r-1].nextSibling,c=null;for(;i<r||o<l;){if(t[i]===s[o]){i++,o++;continue}for(;t[r-1]===s[l-1];)r--,l--;if(r===i){const u=l<n?o?s[o-1].nextSibling:s[l-o]:f;for(;o<l;)e.insertBefore(s[o++],u)}else if(l===o)for(;i<r;)(!c||!c.has(t[i]))&&t[i].remove(),i++;else if(t[i]===s[l-1]&&s[o]===t[r-1]){const u=t[--r].nextSibling;e.insertBefore(s[o++],t[i++].nextSibling),e.insertBefore(s[--l],u),t[r]=s[l]}else{if(!c){c=new Map;let a=o;for(;a<l;)c.set(s[a],a++)}const u=c.get(t[i]);if(u!=null)if(o<u&&u<l){let a=i,d=1,w;for(;++a<r&&a<l&&!((w=c.get(t[a]))==null||w!==u+d);)d++;if(d>u-o){const m=t[i];for(;o<u;)e.insertBefore(s[o++],m)}else e.replaceChild(s[o++],t[i++])}else i++;else t[i++].remove()}}}const ie="_$DX_DELEGATE";function Ne(e,t,s,n={}){let r;return J(l=>{r=l,t===document?e():h(t,e(),t.firstChild?null:void 0,s)},n.owner),()=>{r(),t.textContent=""}}function b(e,t,s){let n;const r=()=>{const i=document.createElement("template");return i.innerHTML=e,i.content.firstChild},l=()=>(n||(n=r())).cloneNode(!0);return l.cloneNode=l,l}function X(e,t=window.document){const s=t[ie]||(t[ie]=new Set);for(let n=0,r=e.length;n<r;n++){const l=e[n];s.has(l)||(s.add(l),t.addEventListener(l,Pe))}}function B(e,t){t==null?e.removeAttribute("class"):e.className=t}function je(e,t,s,n){Array.isArray(s)?(e[`$$${t}`]=s[0],e[`$$${t}Data`]=s[1]):e[`$$${t}`]=s}function we(e,t,s){return E(()=>e(t,s))}function h(e,t,s,n){if(s!==void 0&&!n&&(n=[]),typeof t!="function")return q(e,t,n,s);D(r=>q(e,t(),r,s),n)}function Pe(e){const t=`$$${e.type}`;let s=e.composedPath&&e.composedPath()[0]||e.target;for(e.target!==s&&Object.defineProperty(e,"target",{configurable:!0,value:s}),Object.defineProperty(e,"currentTarget",{configurable:!0,get(){return s||document}});s;){const n=s[t];if(n&&!s.disabled){const r=s[`${t}Data`];if(r!==void 0?n.call(s,r,e):n.call(s,e),e.cancelBubble)return}s=s._$host||s.parentNode||s.host}}function q(e,t,s,n,r){for(;typeof s=="function";)s=s();if(t===s)return s;const l=typeof t,i=n!==void 0;if(e=i&&s[0]&&s[0].parentNode||e,l==="string"||l==="number"){if(l==="number"&&(t=t.toString(),t===s))return s;if(i){let o=s[0];o&&o.nodeType===3?o.data!==t&&(o.data=t):o=document.createTextNode(t),s=N(e,s,n,o)}else s!==""&&typeof s=="string"?s=e.firstChild.data=t:s=e.textContent=t}else if(t==null||l==="boolean")s=N(e,s,n);else{if(l==="function")return D(()=>{let o=t();for(;typeof o=="function";)o=o();s=q(e,o,s,n)}),()=>s;if(Array.isArray(t)){const o=[],f=s&&Array.isArray(s);if(ee(o,t,s,r))return D(()=>s=q(e,o,s,n,!0)),()=>s;if(o.length===0){if(s=N(e,s,n),i)return s}else f?s.length===0?oe(e,o,n):De(e,s,o):(s&&N(e),oe(e,o));s=o}else if(t.nodeType){if(Array.isArray(s)){if(i)return s=N(e,s,n,t);N(e,s,null,t)}else s==null||s===""||!e.firstChild?e.appendChild(t):e.replaceChild(t,e.firstChild);s=t}}return s}function ee(e,t,s,n){let r=!1;for(let l=0,i=t.length;l<i;l++){let o=t[l],f=s&&s[e.length],c;if(!(o==null||o===!0||o===!1))if((c=typeof o)=="object"&&o.nodeType)e.push(o);else if(Array.isArray(o))r=ee(e,o,f)||r;else if(c==="function")if(n){for(;typeof o=="function";)o=o();r=ee(e,Array.isArray(o)?o:[o],Array.isArray(f)?f:[f])||r}else e.push(o),r=!0;else{const u=String(o);f&&f.nodeType===3&&f.data===u?e.push(f):e.push(document.createTextNode(u))}}return r}function oe(e,t,s=null){for(let n=0,r=t.length;n<r;n++)e.insertBefore(t[n],s)}function N(e,t,s,n){if(s===void 0)return e.textContent="";const r=n||document.createTextNode("");if(t.length){let l=!1;for(let i=t.length-1;i>=0;i--){const o=t[i];if(r!==o){const f=o.parentNode===e;!l&&!i?f?e.replaceChild(r,o):e.insertBefore(r,s):f&&o.remove()}else l=!0}}else e.insertBefore(r,s);return[r]}var Ue=b('<span class="border-x-[2px] border-b-[2px] p-1 break-all">'),Le=b('<div class=contents><span class="border-l-[2px] border-b-[2px] p-1">'),Ve=b('<div class="grid grid-cols-[max-content_1fr] border-t-[2px] min-w-fit">'),Be=b('<div class="grid grid-cols-[max-content_1fr]">');const te=(e,t=!0)=>{if(typeof e!="object"||e===null)return(()=>{var n=Ue();return h(n,()=>typeof e=="string"?`'${e}'`:JSON.stringify(e)),n})();const s=Object.entries(e).map(([n,r])=>(()=>{var l=Le(),i=l.firstChild;return h(i,n),h(l,(()=>{var o=k(()=>!!(Array.isArray(r)||typeof r=="object"));return()=>(o(),te(r,!1))})(),null),l})());return t?(()=>{var n=Ve();return h(n,s),n})():(()=>{var n=Be();return h(n,s),n})()};function xe(e){try{if(JSON.parse(e).screen)return!0}catch{return!1}return!1}const Ge=e=>{let t="";if(e.hasOwnProperty("tool_calls")){const s=e.tool_calls[0];let n={};try{n=JSON.parse(s.function.arguments)}catch{}const r=s.function.name;if(t+=`${r}`,n.hasOwnProperty("actions"))for(const l of n.actions)t+=`
 · ${l.action_type} ${l.target_id}`,l.hasOwnProperty("value")&&(t+=` ${l.value}`)}else if(e.role==="tool")return"done";return t};var Je=b('<div class="border-4 rounded-full w-6 h-6 border-gray-500">'),Re=b('<div class="border-4 w-6 h-6 border-gray-500">'),He=b('<div><div class="flex w-full overflow-hidden"><div class="flex-none flex"></div><div class="flex flex-col overflow-hidden w-full">'),Fe=b('<div class="w-[1px] bg-gray-300">'),Ke=b('<div class="absolute left-1/2 top-5 flex justify-center -bottom-3 -translate-x-1/2">'),qe=b('<div class="flex-none h-6 flex items-center"><div class="h-2 w-2 rounded-full bg-gray-300">'),Qe=b('<div class="text-xs my-1 font-semibold">'),We=b("<div><button>View"),Xe=b('<div><div class="flex-1 text-xs text-gray-500 overflow-x-auto scrollbar-rounded overflow-hidden whitespace-pre-wrap"></div><div class="flex-none ml-4 px-10 w-16 flex justify-center">'),Ye=b('<div class="text-base whitespace-pre-wrap">'),Ze=b('<div><div class="flex h-full"><div class="relative flex-none h-full mx-2 w-2 flex"></div><div class="w-full overflow-hidden">');function ze(e){const t=s=>{if(s.role!=="tool")return!1;const n=JSON.parse(s.content);return n.hasOwnProperty("session_id")?n.hasOwnProperty("error_info"):!0};return(()=>{var s=He(),n=s.firstChild,r=n.firstChild,l=r.nextSibling;return h(r,A(Oe,{get children(){return[A(re,{get when(){return e.indexedMessageGroup[0].message.role==="user"},get children(){return Je()}}),A(re,{get when(){return e.indexedMessageGroup[0].message.role==="assistant"},get children(){return Re()}})]}})),h(l,A(be,{get each(){return e.indexedMessageGroup},children:(i,o)=>(()=>{var f=Ze(),c=f.firstChild,u=c.firstChild,a=u.nextSibling;return h(u,A(j,{get when(){return e.indexedMessageGroup.length>1},get children(){return[(()=>{var d=Ke();return h(d,A(j,{get when(){return o()!==e.indexedMessageGroup.length-1},get children(){return Fe()}})),d})(),qe()]}})),h(a,A(j,{get when(){return i.message.tool_calls||i.message.role==="tool"},get children(){return[(()=>{var d=Qe();return h(d,()=>i.message.tool_calls?"call":"tool",null),h(d,()=>t(i.message)?" error!!!":"",null),d})(),(()=>{var d=Xe(),w=d.firstChild,m=w.nextSibling;return h(w,(()=>{var x=k(()=>e.detail===!0);return()=>x()?te(i.message):Ge(i.message)})()),h(m,A(j,{get when(){return xe(i.message.content)},get children(){var x=We(),C=x.firstChild;return C.$$click=()=>e.setViewIndex(i.index),D(y=>{var g=e.viewIndex===i.index,p=`${e.viewIndex===i.index?"bg-gray-300":"hover:bg-gray-200"}  border-gray-400 w-16 border-2 rounded-2xl py-1 text-xs font-semibold text-gray-400`;return g!==y.e&&(C.disabled=y.e=g),p!==y.t&&B(C,y.t=p),y},{e:void 0,t:void 0}),x}})),D(()=>B(d,`flex
                                                    ${e.detail===!0?"items-center":"items-start"} overflow-hidden`)),d})()]}}),null),h(a,A(j,{get when(){return i.message.role!=="tool"&&i.message.content},get children(){var d=Ye();return h(d,()=>i.message.content),d}}),null),D(()=>B(f,o()===0?"":"mt-2")),f})()})),D(()=>B(s,`flex px-6 py-4 ${e.indexedMessageGroup[0].message.role==="assistant"?"bg-gray-100":""}`)),s})()}X(["click"]);var et=b('<div class="h-full p-4 min-h-56"><div class="flex h-full flex-col rounded-3xl border-2 border-black overflow-hidden"><div class="relative border-b-2 border-black py-4 text-center rounded-t-3xl"><span class="text-2xl font-semibold">Dialog</span><label class="absolute right-2 bottom-1 flex justify-end items-center"><div class="h-4 w-4 rounded-full ring-2 ring-gray-700 flex justify-center items-center"></div><span class="ml-1 text-gray-700 text-base">detail</span></label></div><div class="overflow-y-auto scrollbar-rounded">'),tt=b('<div class="h-2 w-2 rounded-full bg-gray-700">');function st(e){let t;me(()=>{if(e.scrollDownTrigger<=99){t.scrollTo({top:t.scrollHeight,behavior:"smooth"});return}t.scrollHeight-t.scrollTop<=t.clientHeight+150&&t.scrollTo({top:t.scrollHeight,behavior:"smooth"})});const s=k(()=>{const l=[];let i=null;const o=e.messages.map((f,c)=>({message:f,index:c}));for(let f of o)switch(f.message.role){case"user":i==="user"?l[l.length-1].push(f):(l.push([f]),i="user");break;case"assistant":i==="assistant"?l[l.length-1].push(f):(l.push([f]),i="assistant");break;case"tool":l[l.length-1].push(f);break}return l}),[n,r]=P(!1);return(()=>{var l=et(),i=l.firstChild,o=i.firstChild,f=o.firstChild,c=f.nextSibling,u=c.firstChild,a=o.nextSibling;c.$$click=()=>{r(!n())},h(u,(()=>{var w=k(()=>!!n());return()=>w()?tt():""})());var d=t;return typeof d=="function"?we(d,a):t=a,h(a,A(be,{get each(){return s()},children:w=>A(ze,{indexedMessageGroup:w,get viewIndex(){return e.viewIndex},get setViewIndex(){return e.setViewIndex},get detail(){return n()}})})),l})()}X(["click"]);var nt=b("<div class=text-left>"),lt=b('<div class="my-6 rounded-xl border-2 border-dotted border-gray-500 px-4 py-2">'),rt=b('<span class="inline-block min-h-10 max-w-full p-2 m-1 text-base rounded-xl text-gray-800 whitespace-pre-wrap bg-gray-100 break-words">'),it=b('<div class="relative my-2 inline-block w-full"><button type=button class="bg-[radial-gradient(circle,_#D1D5DB_1px,_transparent_1px)] bg-[size:3px_3px] whitespace-normal break-words rounded-xl border-2 border-gray-500 px-3 py-2 text-base text-gray-800 font-semibold hover:bg-gray-300 w-full min-h-12"></button><span class="absolute -top-2 -right-2 flex h-6 w-6 items-center justify-center rounded-full border-2 border-gray-500 bg-white text-xs font-semibold text-gray-800">'),ot=b('<div class="relative my-2 inline-block w-full text-left"><div class="px-3 py-2 border-2 border-gray-500 rounded-xl max-h-48 overflow-auto scrollbar-rounded"><div class="flex justify-between"><span class="pb-1 text-base font-semibold text-gray-800"></span><span class="text-xs text-gray-500"></span></div><div class="whitespace-pre-wrap border-b-2 resize-none outline-none text-base text-gray-800 focus:border-gray-500"contenteditable=plaintext-only></div></div><span class="absolute -top-2 -right-2 flex h-6 w-6 items-center justify-center rounded-full border-2 border-gray-500 bg-white text-xs font-semibold text-gray-800">'),at=b('<div class="h-full p-4 min-h-96"><div class="flex h-full flex-col justify-between rounded-3xl border-2 border-black"><div class=" border-b-2 border-black py-4 text-center rounded-t-3xl"><span class="text-2xl font-semibold">Screen</span></div><div class="relative border-t-2 border-black"><div class="flex justify-center py-8 text-center"><button class="w-44 border-r-2 border-white rounded-l-2xl pl-2 py-1 text-lg font-semibold text-white bg-gray-950 hover:bg-gray-600">New Session</button><button class="w-28 border-l-1 border-white rounded-r-2xl py-1 text-lg font-semibold text-white bg-gray-950 hover:bg-gray-600">Display</button></div><div class="absolute right-0 bottom-0 left-0 text-center text-xs text-gray-400 pb-0.5">'),ct=b('<div class="flex-1 overflow-y-auto scrollbar-rounded py-2 px-4 text-center ${}">'),ut=b('<div class="bg-stripes-45 w-full h-full">');function ft(e){const t=new DOMParser,s=k(()=>{if(!e.content)return{};const c=JSON.parse(e.content),u=t.parseFromString(c.screen,"text/html");return{session_id:c.session_id,screen:n(u.body)}}),n=c=>{const u=nt();return r(u,c.childNodes),u},r=(c,u)=>{for(let a of u)switch(a.nodeName){case"DIV":c.appendChild(l(a)),l(a);break;case"INPUT":c.appendChild(f(a));break;case"BUTTON":c.appendChild(o(a));break;case"SPAN":c.appendChild(i(a));break}},l=c=>{const u=lt();return r(u,c.childNodes),u},i=c=>(()=>{var u=rt();return h(u,()=>c.textContent),u})(),o=c=>(()=>{var u=it(),a=u.firstChild,d=a.nextSibling;return a.$$click=()=>e.execute(s().session_id,[{action_type:"press",target_id:c.id}]),h(a,()=>c.innerText),h(d,()=>c.id),u})(),f=c=>{let u=c.getAttribute("value"),a=c.getAttribute("type");return a==="number"&&(c.getAttribute("step")==="1"?a="int":a="float"),(()=>{var d=ot(),w=d.firstChild,m=w.firstChild,x=m.firstChild,C=x.nextSibling,y=m.nextSibling,g=w.nextSibling;return h(x,()=>c.name),h(C,a),y.addEventListener("blur",p=>{const $=p.target.textContent;if(u===$)return;const M=[];M.push({action_type:"fill",target_id:c.id,value:$}),e.execute(s().session_id,M),u=$}),y.$$keydown=p=>{p.key==="Enter"&&!p.shiftKey&&(p.preventDefault(),p.target.blur())},h(y,()=>c.getAttribute("value")),h(g,()=>c.id),d})()};return(()=>{var c=at(),u=c.firstChild,a=u.firstChild,d=a.nextSibling,w=d.firstChild,m=w.firstChild,x=m.nextSibling,C=w.nextSibling;return h(u,(()=>{var y=k(()=>!!s().hasOwnProperty("screen"));return()=>y()?(()=>{var g=ct();return h(g,()=>s().screen),g})():ut()})(),d),je(m,"click",e.newSession),x.$$click=()=>e.display(s().session_id),h(C,(()=>{var y=k(()=>!!s().session_id);return()=>y()?`session_id: ${s().session_id}`:""})()),c})()}X(["click","keydown"]);const G="";class dt{constructor(){const[t,s]=P([]);this._messages=t,this._setMessages=s;const[n,r]=P(-1);this._viewIndex=n,this._setViewIndex=r;const[l,i]=P(0);this._scrollDownTrigger=l,this._setIsScrollDownTrigger=i,this._user_call_count=0}get messages(){return this._messages}get viewIndex(){return this._viewIndex}get setViewIndex(){return this._setViewIndex}get scrollDownTrigger(){return this._scrollDownTrigger}_setMessagesAndScrollDown(t,s=!0){this._setMessages(t),this._setIsScrollDownTrigger(n=>s?n>=99?0:n+1:n+100)}async addUserMessage(t){this._setMessagesAndScrollDown(n=>[...n,{role:"user",content:t}]),await this._predict();let s=0;for(;s<5&&this._messages()[this._messages().length-1].hasOwnProperty("tool_calls");)await this._call(),await this._predict(),s+=1}async _predict(){const t={role:"assistant",content:""};this._setMessagesAndScrollDown(o=>[...o,t]);const s=await fetch(`${G}/completions`,{method:"POST",headers:{"Content-Type":"application/json",Accept:"text/event-stream, application/json"},body:JSON.stringify({messages:this._messages().slice(0,-1)})});if(!s.ok)throw new Error(`HTTP error! status: ${s.status}`);const n=s.headers.get("Content-Type");if(n==="application/json")throw new Error(`Server error: ${await s.json()}`);if(typeof n=="string"&&!n.includes("text/event-stream"))throw new Error(`Unexpected content type: ${n}`);const r=s.body.getReader(),l=new TextDecoder;let i="";for(;;){const{done:o,value:f}=await r.read();if(o)break;const c=l.decode(f);for(i+=c;;){const u=i.indexOf(`

`);if(u===-1)break;const a=i.slice(0,u);i=i.slice(u+2);const d=a.slice(6),w=JSON.parse(d);if(w.choices[0].finish_reason!==null)return;const x=w.choices[0].delta,C=x.content,y=x.tool_calls;if(C!==null)t.hasOwnProperty("content")||(t.content=""),t.content+=C,this._setMessagesAndScrollDown(g=>{const p=g[g.length-1];return p.hasOwnProperty("content")||(p.content=""),p.content=t.content,[...g]},!1);else if(y!==null){const g=y[0],p=g.index,$=g.id,M=g.function.name,V=g.function.arguments,ne=g.type;this._setMessagesAndScrollDown(Y=>{const I=Y[Y.length-1];return I.hasOwnProperty("tool_calls")||(I.tool_calls=[{}]),p!==null&&(I.tool_calls[0].index=p),$!==null&&(I.tool_calls[0].id=$),M!==null&&(I.tool_calls[0].function={name:M}),V!==null&&(I.tool_calls[0].function.hasOwnProperty("arguments")||(I.tool_calls[0].function.arguments=""),I.tool_calls[0].function.arguments+=V),ne!==null&&(I.tool_calls[0].type=ne),[...Y]},!1)}else console.error("Unknown delta: ",x)}}}async addUserNewSessionMessage(){const t=this._getUserCallId();this._setMessagesAndScrollDown(s=>[...s,{role:"user",tool_calls:[{index:"0",id:t,function:{name:"new_session",arguments:"{}"},type:"function"}]}]),await this._call()}async addUserDisplayMessage(t){const s=this._getUserCallId();this._setMessagesAndScrollDown(n=>[...n,{role:"user",tool_calls:[{index:"0",id:s,function:{name:"display",arguments:JSON.stringify({session_id:t})},type:"function"}]}]),await this._call()}async addUserExecuteMessage(t,s){const n=this._getUserCallId();this._setMessagesAndScrollDown(r=>[...r,{role:"user",tool_calls:[{id:n,function:{name:"execute",arguments:JSON.stringify({session_id:t,actions:s})},type:"function"}]}]),await this._call()}_getUserCallId(){return`user_call_${this._user_call_count++}`}async _call(){const t=this._messages()[this._messages().length-1];if(!t.hasOwnProperty("tool_calls"))return;const s=t.tool_calls[0].id,n=t.tool_calls[0].function.name,r=t.tool_calls[0].function.arguments;let l="";switch(n){case"new_session":l=`${G}/session`;break;case"display":l=`${G}/display`;break;case"execute":l=`${G}/execute`;break;default:console.error("Unknown function name: ",n);return}let o=await(await fetch(l,{method:"POST",headers:{"Content-Type":"application/json"},body:r})).text();this._setMessagesAndScrollDown(f=>[...f,{role:"tool",content:o,tool_call_id:s}]),xe(o)===!0&&this.setViewIndex(this.messages().length-1)}}var ht=b('<div class="px-4 pb-4 w-full text-left"><div class="flex pl-6 pr-2 border-2 border-black rounded-3xl overflow-y-hidden"><div class="flex-1 min-h-10 max-h-32 overflow-y-auto scrollbar-rounded"><div class=" my-2 resize-none outline-none text-base text-gray-800"contenteditable=plaintext-only></div></div><div class="flex-none flex justify-center items-end"><button class="group ml-4 mb-1 flex items-center justify-center w-8 h-8 border-4 border-gray-950 rounded-full py-1 text-xs font-semibold text-gray-400 hover:border-gray-600"><div class="w-4 h-4 bg-gray-950 rounded-full group-hover:bg-gray-600">');function gt(e){let t;const s=()=>{const n=t.textContent;n.trim()!==""&&(t.textContent="",e.send(n))};return(()=>{var n=ht(),r=n.firstChild,l=r.firstChild,i=l.firstChild,o=l.nextSibling,f=o.firstChild;i.$$keydown=u=>{u.key==="Enter"&&!u.shiftKey&&(u.preventDefault(),s())};var c=t;return typeof c=="function"?we(c,i):t=i,f.$$click=s,n})()}X(["keydown","click"]);var pt=b('<div class="flex h-screen"><div class="flex flex-1 flex-col justify-between min-h-96 min-w-96"><div class="flex-1 overflow-hidden"></div><div class=flex-none></div></div><div class="h-screen w-96 flex-none">');function bt(){const e=new dt;return(()=>{var t=pt(),s=t.firstChild,n=s.firstChild,r=n.nextSibling,l=s.nextSibling;return h(n,A(st,{get messages(){return e.messages()},get viewIndex(){return e.viewIndex()},get setViewIndex(){return e.setViewIndex},get scrollDownTrigger(){return e.scrollDownTrigger()}})),h(r,A(gt,{send:i=>e.addUserMessage(i)})),h(l,A(ft,{get content(){return k(()=>e.viewIndex()!==-1)()?e.messages()[e.viewIndex()].content:""},newSession:()=>e.addUserNewSessionMessage(),display:i=>e.addUserDisplayMessage(i),execute:(i,o)=>e.addUserExecuteMessage(i,o)})),t})()}const wt=document.getElementById("root");Ne(()=>A(bt,{}),wt);
