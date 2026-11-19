const { loadModule } = require('hunspell-asm/dist/cjs/index.js');
window.nactiHunspell = async (affBuf, dicBuf) => {
  const f = await loadModule();
  const aff = f.mountBuffer(new Uint8Array(affBuf), 'cs.aff');
  const dic = f.mountBuffer(new Uint8Array(dicBuf), 'cs.dic');
  return f.create(aff, dic);
};
