// plugins/polyfill.client.ts
export default defineNuxtPlugin(() => {
  // فقط اگر واقعاً وجود نداره polyfill کن
  if (typeof globalThis.File === 'undefined') {
    globalThis.File = class File extends Blob {
      name: string = ''
      lastModified: number = 0

      constructor(
        fileBits: BlobPart[],
        fileName: string,
        options?: FilePropertyBag
      ) {
        super(fileBits, options)
        this.name = fileName
        this.lastModified = options?.lastModified ?? Date.now()
      }
    } as typeof File // برای type-safety بهتر
  }
})