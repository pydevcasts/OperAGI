// server/api/auth/[...].ts
import { eventHandler } from "h3"
import { getAuth, createFetchRequest } from "~/server/utils/auth"

export default eventHandler(async (event) => {
  const auth = getAuth()

  console.log('=== Auth Request ===')
  console.log('URL:', event.node.req.url)
  console.log('Method:', event.node.req.method)
  console.log('====================')

  try {
    // ایجاد درخواست سازگار با Fetch API
    const fetchRequest = await createFetchRequest(event)
    
    // ایجاد پروکسی برای سازگاری کامل
    const proxyReq = new Proxy(event.node.req, {
      get(target, prop) {
        if (prop in fetchRequest) {
          return (fetchRequest as any)[prop]
        }
        return Reflect.get(target, prop)
      }
    })

    const result = await auth.handler(proxyReq, event.node.res)
    
    console.log('=== Auth Handler Result ===')
    console.log('Status:', result.status)
    console.log('===========================')
    
    return result
  } catch (error) {
    console.error('=== Auth Handler Error ===')
    console.error('Error:', error)
    console.error('===========================')
    throw error
  }
})