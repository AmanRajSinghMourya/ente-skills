// Paste into the built-in browser's javascript_tool on the console's "create" page
// after switching the editor to JSON View. Replace __PAYLOAD__ with the payload
// object (not a string). form_input stores "[object Object]"; typing drops chars.
(() => {
  const ta = document.querySelector('textarea.npm__react-simple-code-editor__textarea');
  if (!ta) return 'no editor: click "JSON View" first';
  const value = JSON.stringify(__PAYLOAD__, null, 2);
  Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, 'value').set.call(ta, value);
  ta.dispatchEvent(new Event('input', { bubbles: true }));
  ta.focus();
  ta.setSelectionRange(ta.value.length, ta.value.length);
  return ta.value.length;
})()
