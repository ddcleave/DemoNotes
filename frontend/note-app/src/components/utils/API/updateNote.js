import { baseurl } from "./baseurl"
import refreshAPI from "./refresh"

export default async function updateNoteAPI(id, data) {
  const url = `/note/note/${id}`
  const formData = new FormData()
  formData.append('note', JSON.stringify(data))
  const response = await refreshAPI(
    async () => await fetch(baseurl + url, {
      method: "put",
      headers: {},
      body: formData,
    })
  )
  return response
}