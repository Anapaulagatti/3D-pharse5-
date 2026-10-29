// Deployment-only save isolation: GitHub project Pages share one browser origin.
const reviewPrefix = "korean-pixel-town-pages-review:";
const scoped = (key) => {
  const value = String(key);
  return value.startsWith("korean-arena-") ||
    value.startsWith("review-only-v1:korean-arena-")
    ? reviewPrefix + value
    : value;
};
const read = window.Storage.prototype.getItem;
const write = window.Storage.prototype.setItem;
const remove = window.Storage.prototype.removeItem;
window.Storage.prototype.getItem = function (key) {
  return read.call(this, scoped(key));
};
window.Storage.prototype.setItem = function (key, value) {
  return write.call(this, scoped(key), value);
};
window.Storage.prototype.removeItem = function (key) {
  return remove.call(this, scoped(key));
};
