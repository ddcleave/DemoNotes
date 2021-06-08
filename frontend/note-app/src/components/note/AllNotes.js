import Grid from '@material-ui/core/Grid';
import { useSelector, useDispatch } from 'react-redux'
import { useEffect, useState } from 'react';
import PreviewNote from './PreviewNote';
import GlobalEditNote from './GlobalEditNote';
import useInfiniteScroll from 'react-infinite-scroll-hook';
import { Container } from '@material-ui/core';
import { getNotes, getTags, setLoading } from './notesSlice';
import { makeStyles } from '@material-ui/core/styles';


const useStyles = makeStyles((theme) => ({
  cardGrid: {
    marginTop: theme.spacing(2),
    paddingTop: theme.spacing(8),
    paddingBottom: theme.spacing(8)
  }
}))

function NoteGrid() {
  const classes = useStyles()
  const note_db = useSelector((state) => state.notes.note_db)
  const openTag = useSelector((state) => state.tag.name)
  const all_note_ids = useSelector((state) => state.notes.all.note_ids)
  const tags = useSelector((state) => state.notes.tags[openTag])

  const note_ids = (openTag === '') ?
    all_note_ids :
    tags.note_ids

  return (
    <Container className={classes.cardGrid} maxWidth='md'>
      <Grid container spacing={4}>
        {note_ids.map((note_id) => (
          <Grid item key={note_db[note_id].version} xs={12} sm={6} md={4}>
            <PreviewNote
              id={note_id}
              datanote={note_db[note_id].data}
              tagged={note_db[note_id].tags}
            />
          </Grid>
        ))}
      </Grid>
    </Container>
  )
}


function LoadNewNotes() {
  const note_db = useSelector((state) => state.notes.note_db)
  const openTag = useSelector((state) => state.tag.name)
  const all_loading = useSelector((state) => state.notes.all.loading)
  const tags = useSelector((state) => state.notes.tags)
  const full = useSelector((state) => state.notes.all.full)
  const all_note_ids = useSelector((state) => state.notes.all.note_ids)
  const status = useSelector((state) => state.notes.all.status)
  const dispatch = useDispatch()
  const loading = (openTag === '') ?
    all_loading :
    tags[openTag].loading

  const hasNextPage = (openTag === '') ?
    (!full && (status === 'secceeded')) :
    (!(tags[openTag].full) && (tags[openTag].status === 'secceeded'))

  async function loadMore() {
    const last_note_id = (openTag === '') ?
      all_note_ids.slice(-1)[0] :
      tags[openTag].note_ids.slice(-1)[0]
    if (last_note_id) {
      setLoading({ tag: openTag, load: true })
      dispatch(getNotes({ position: note_db[last_note_id].position, tag: openTag }))
      setLoading({ tag: openTag, load: false });
    }
  }

  const [sentryRef] = useInfiniteScroll({
    loading,
    hasNextPage,
    onLoadMore: loadMore,
    rootMargin: '0px 0px 400px 0px',
  })

  return (<div ref={sentryRef} />)
}

export default function AllNotes() {
  const status = useSelector((state) => state.notes.status)
  const openTag = useSelector((state) => state.tag.name)
  const status_all_notes = useSelector((state) => state.notes.all.status)
  const tags = useSelector((state) => state.notes.tags)
  const dispatch = useDispatch()

  useEffect(() => {
    if (status === 'idle') {
      dispatch(getTags())
    }
  }, [status])

  useEffect(() => {
    if (status === 'secceeded') {
      if (openTag === '') {
        if (status_all_notes === 'idle') {
          dispatch(getNotes({ position: null, tag: '' }))
        }
      }
      else {
        if (tags[openTag].status === 'idle') {
          dispatch(getNotes({ position: null, tag: openTag }))
        }
      }
    }

  }, [status, openTag, status_all_notes, tags])

  return (
    <>
      <NoteGrid />
      <LoadNewNotes />
      <GlobalEditNote />
    </>
  )
}
