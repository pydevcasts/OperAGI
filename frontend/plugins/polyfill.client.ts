// plugins/polyfill.client.ts
if (typeof File === 'undefined') {
  (globalThis as any).File = class File extends Blob {
    name: string
    lastModified: number

    constructor(fileBits: BlobPart[], fileName: string, options?: FilePropertyBag) {
      super(fileBits, options)
      this.name = fileName
      this.lastModified = options?.lastModified ?? Date.now()
    }
  }
}