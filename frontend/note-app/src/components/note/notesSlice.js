import { createAsyncThunk, createSlice } from '@reduxjs/toolkit'
import { nanoid } from 'nanoid'
import addTagAPI from '../utils/API/addTag'
import createNoteAPI from '../utils/API/createNote'
import createTagAPI from '../utils/API/createTag'
import deleteNoteAPI from '../utils/API/deleteNote'
import getNotesAPI from '../utils/API/getNotes'
import getTagsAPI from '../utils/API/getTags'
import removeTagAPI from '../utils/API/removeTag'
import updateNoteAPI from '../utils/API/updateNote'


const initialState = {
  status: 'idle',
  note_db: {},
  tags: {},
  all: {
    status: 'idle',
    note_ids: [],
    full: false,
    loading: false
  }
}

export const getNotes = createAsyncThunk(
  'notes/getNotes',
  async (userData) => {
    const { position, tag } = userData
    const response = await getNotesAPI(position, tag)
    const data = await response.json()
    return data
  }
)


export const getTags = createAsyncThunk(
  'notes/getTags',
  async () => {
    const response = await getTagsAPI()
    const data = await response.json()
    return data
  }
)

export const addNote = createAsyncThunk(
  'notes/addNote',
  async (userData) => {
    const {savedData, tags} = userData
    const response = await createNoteAPI(savedData, tags)
    const data = await response.json()
    return data
  }
)

export const deleteNote = createAsyncThunk(
  'notes/deleteNote',
  async (id) => {
    const response = await deleteNoteAPI(id)
    const data = await response.json()
    return data
  }
)

export const updateNote = createAsyncThunk(
  'notes/updateNote',
  async (userData) => {
    const { id, savedData } = userData
    const response = await updateNoteAPI(id, savedData)
    const data = await response.json()
    return data
  }
)

export const createTag = createAsyncThunk(
  'notes/createTag',
  async (tag) => {
    const response = await createTagAPI(tag)
    const data = await response.json()
    return data
  }
)

export const addTagToNote = createAsyncThunk(
  'notes/addTagToNote',
  async (userData) => {
    const { noteid, tag } = userData
    const response = await addTagAPI(noteid, tag)
    const data = await response.json()
    return data
  }
)

export const removeTagFromNote = createAsyncThunk(
  'notes/removeTagFromNote',
  async (userData) => {
    const { noteid, tag } = userData
    const response = await removeTagAPI(noteid, tag)
    const data = await response.json()
    return data
  }
)

const notesSlice = createSlice({
  name: 'notes',
  initialState,
  reducers: {
    setLoading(state, action) {
      const { tag, load } = action.payload
      if (tag === '') {
        state.all.loading = load
      }
      else {
        state.tags[tag].loading = load
      }
    },
    resetData(state, action) {}
  },
  extraReducers: {
    [getNotes.pending]: (state, action) => {
      const params = action.meta.arg
      if (params.tag === '') {
        state.all.status = 'loading'
      }
      else {
        state.tags[params.tag].status = 'loading'
      }
    },
    [getNotes.fulfilled]: (state, action) => {
      const params = action.meta.arg
      if (params.tag === '') {
        // state.all.status = 'secceeded'

        if (action.payload.length === 0) {
          state.all.full = true
        }
        else {
          for (let note of action.payload) {
            const array_tags = note.tags.map((tag) => tag.label)
            state.note_db[note.id] = {
              create_data: note.note.create_data,
              creator: note.note.creator,
              data: JSON.parse(note.note.data),
              token: note.note.token,
              position: note.position,
              shared: note.shared,
              tags: array_tags,
              version: nanoid()
            }
            state.all.note_ids.push(note.id)
          }
        }
        state.all.status = 'secceeded'
      }
      else {
        if (action.payload.length === 0) {
          state.tags[params.tag].full = true
        }
        else {
          for (let note of action.payload) {
            const array_tags = note.tags.map((tag) => tag.label)
            state.note_db[note.id] = {
              create_data: note.note.create_data,
              creator: note.note.creator,
              data: JSON.parse(note.note.data),
              token: note.note.token,
              position: note.position,
              shared: note.shared,
              tags: array_tags,
              version: nanoid()
            }
            state.tags[params.tag].note_ids.push(note.id)
          }
        }
        state.tags[params.tag].status = 'secceeded'
      }
    },
    [getNotes.rejected]: (state, action) => {
      const params = action.meta.arg
      if (params.tag === '') {
        state.all.status = 'failed'
      }
      else {
        state.tags[params.tag].status = 'failed'
      }
    },
    [getTags.rejected]: (state, action) => {
      state.status = 'failed'
    },
    [getTags.fulfilled]: (state, action) => {
      state.status = 'secceeded'
      for (let tag of action.payload) {
        state.tags[tag.label] = {
          status: 'idle',
          note_ids: [],
          full: false,
          loading: false
        }
      }
    },
    [getTags.rejected]: (state, action) => {
      state.status = 'failed'
    },
    [addNote.fulfilled]: (state, action) => {
      const note = action.payload
      const array_tags = note.tags.map((tag) => tag.label)
      state.note_db[note.id] = {
        create_data: note.note.create_data,
        creator: note.note.creator,
        data: JSON.parse(note.note.data),
        token: note.note.token,
        position: note.position,
        shared: note.shared,
        tags: array_tags,
        version: nanoid()
      }
      state.all.note_ids.unshift(note.id)
      for (let tag of array_tags) {
        if (tag in state.tags) {
          if (state.tags[tag].status !== 'idle'){
            state.tags[tag].note_ids.unshift(note.id)
          }
        }
      }
    },
    [deleteNote.fulfilled]: (state, action) => {
      const note = action.payload
      for (let tag of state.note_db[note.id].tags) {
        if (tag in state.tags) {
          const new_arr = state.tags[tag].note_ids.filter((note_id) => note_id !== note.id)
          state.tags[tag].note_ids = new_arr
        }
      }
      const tmp = state.all.note_ids.filter((note_id) => note_id !== note.id)
      state.all.note_ids = tmp
      delete state.note_db[note.id]
    },
    [updateNote.fulfilled]: (state, action) => {
      const note = action.payload
      state.note_db[note.id].data = JSON.parse(note.note.data)
      state.note_db[note.id].version = nanoid()
    },
    [createTag.fulfilled]: (state, action) => {
      const tag = action.payload
      state.tags[tag.label] = {
        status: 'idle',
        note_ids: [],
        full: false,
        loading: false
      }
    },
    [addTagToNote.fulfilled]: (state, action) => {
      const note = action.payload
      state.note_db[note.id].tags = note.tags
      state.note_db[note.id].version = nanoid()
      const params = action.meta.arg
      state.tags[params.tag] = {
        status: 'idle',
        note_ids: [],
        full: false,
        loading: false
      }
    },
    [removeTagFromNote.fulfilled]: (state, action) => {
      const note = action.payload
      state.note_db[note.id].tags = note.tags
      state.note_db[note.id].version = nanoid()
      const params = action.meta.arg
      const arr = state.tags[params.tag].note_ids.filter((item) => item.id !== params.noteid)
      if (arr.length === 0) {
        state.tags[params.tag] = {
          status: 'idle',
          note_ids: [],
          full: false,
          loading: false
        }
      }
      else {
        state.tags[params.tag] = arr
      }
    }
  },
})

export const { setLoading, resetData } = notesSlice.actions

export default notesSlice.reducer