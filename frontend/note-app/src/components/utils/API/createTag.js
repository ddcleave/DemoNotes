import { baseurl } from "./baseurl"
import refreshAPI from "./refresh"

export default async function createTagAPI(tag) {
  const url = '/note/tag/create'
  const formData = new FormData()
  formData.append("tag", tag)

  const response = await refreshAPI(
    async () => await fetch(baseurl + url, {
      method: "post",
      headers: {},
      body: formData
    })
  )
  return response
}