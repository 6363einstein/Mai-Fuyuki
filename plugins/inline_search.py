import logging
import asyncio
from pyrogram import Client
from pyrogram.types import (
    InlineQuery,
    InlineQueryResultArticle,
    InlineQueryResultPhoto,
    InputTextMessageContent,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from plugins.Dreamxfutures.Imdbposter import _tmdb_get, TMDB_IMAGE_BASE_URL, MIN_RUNTIME
from info import TMDB_API_KEY
from datetime import datetime

logger = logging.getLogger(__name__)

TMDB_BEARER_TOKEN = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2ZGU3YTIyZGU1YjE5YTFjNmUyZGU5ZWEyMzE2ZmQxMCIsIm5iZiI6MTc0NTMyMjQ2Mi41MzMsInN1YiI6IjY4MDc4MWRlYzVjODAzNWZiMDhhNjExNCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.rMMJ2-PBIv8Y7ybxPIEpIlzTEXzuwrm9ruKxAUCAsbw'


async def tmdb_multi_search(query: str, max_results: int = 8):
    """
    Search TMDB for movies/TV shows in a single API call.
    Returns a list of result dicts with title, year, rating, genres, plot, poster_url, tmdb_url, kind.
    """
    params = {
        'query': query,
        'language': 'en-US',
        'page': 1,
        'include_adult': 'false'
    }
    try:
        result = await _tmdb_get('search/multi', params=params, api_key=TMDB_API_KEY or None)
    except Exception as e:
        logger.error(f"TMDB multi search failed: {e}")
        return []

    raw_results = result.get('results', [])
    today = datetime.utcnow().date()
    filtered = []

    for r in raw_results:
        mtype = r.get('media_type')
        if mtype not in ('movie', 'tv'):
            continue
        rd_str = r.get('release_date') or r.get('first_air_date', '')
        try:
            rd_date = datetime.strptime(rd_str[:10], '%Y-%m-%d').date() if rd_str else None
        except ValueError:
            rd_date = None

        title = r.get('title') or r.get('name') or 'Unknown'
        year = rd_str[:4] if rd_str else ''
        rating = round(float(r.get('vote_average', 0)), 1)
        genre_ids = r.get('genre_ids', [])
        plot = r.get('overview') or 'No description available.'
        if len(plot) > 250:
            plot = plot[:250] + '...'
        poster_path = r.get('poster_path')
        poster_url = f"{TMDB_IMAGE_BASE_URL}{poster_path}" if poster_path else None
        tmdb_url = f"https://www.themoviedb.org/{mtype}/{r.get('id')}"
        kind = 'Movie' if mtype == 'movie' else 'TV Series'

        filtered.append({
            'title': title,
            'year': year,
            'rating': rating if rating > 0 else None,
            'plot': plot,
            'poster_url': poster_url,
            'tmdb_url': tmdb_url,
            'kind': kind,
            'popularity': r.get('popularity', 0),
        })

        if len(filtered) >= max_results:
            break

    return filtered


@Client.on_inline_query()
async def inline_search(client, query: InlineQuery):
    search_text = query.query.strip()

    # Empty query — show placeholder
    if not search_text:
        await query.answer(
            results=[
                InlineQueryResultArticle(
                    title="🔍 Search Movie or Series",
                    description="Type a movie or web series name...",
                    input_message_content=InputTextMessageContent(
                        "🔍 Type a movie or series name to search."
                    ),
                )
            ],
            cache_time=0,
        )
        return

    try:
        results = await tmdb_multi_search(search_text, max_results=8)

        if not results:
            await query.answer(
                results=[
                    InlineQueryResultArticle(
                        title="❌ No Results Found",
                        description=f'No results for: "{search_text}"',
                        input_message_content=InputTextMessageContent(
                            f"❌ No results found for <b>{search_text}</b>\n\nTry a different spelling.",
                            parse_mode="html"
                        ),
                    )
                ],
                cache_time=5,
            )
            return

        inline_results = []

        for movie in results:
            try:
                title = movie['title']
                year = movie['year']
                rating = movie['rating']
                plot = movie['plot']
                poster_url = movie['poster_url']
                tmdb_url = movie['tmdb_url']
                kind = movie['kind']

                caption = (
                    f"🎬 <b>{title}</b>"
                    + (f" ({year})" if year else "")
                    + (f"\n📺 <b>Type:</b> {kind}" if kind else "")
                    + (f"\n⭐ <b>Rating:</b> {rating}/10" if rating else "")
                    + f"\n\n📝 {plot}"
                )

                buttons = []
                if tmdb_url:
                    buttons.append([InlineKeyboardButton("🌐 View on TMDB", url=tmdb_url)])
                reply_markup = InlineKeyboardMarkup(buttons) if buttons else None

                title_display = f"🎬 {title}" + (f" ({year})" if year else "")
                description = (f"⭐ {rating}/10 | " if rating else "") + kind

                if poster_url:
                    inline_results.append(
                        InlineQueryResultPhoto(
                            photo_url=poster_url,
                            thumb_url=poster_url,
                            title=title_display,
                            description=description,
                            caption=caption,
                            parse_mode="html",
                            reply_markup=reply_markup,
                        )
                    )
                else:
                    inline_results.append(
                        InlineQueryResultArticle(
                            title=title_display,
                            description=description,
                            input_message_content=InputTextMessageContent(
                                caption, parse_mode="html"
                            ),
                            reply_markup=reply_markup,
                        )
                    )
            except Exception as e:
                logger.warning(f"Skipping result due to error: {e}")
                continue

        if not inline_results:
            await query.answer(
                results=[
                    InlineQueryResultArticle(
                        title="❌ No Results Found",
                        description=f'No results for: "{search_text}"',
                        input_message_content=InputTextMessageContent(
                            f"❌ No results found for <b>{search_text}</b>",
                            parse_mode="html"
                        ),
                    )
                ],
                cache_time=5,
            )
            return

        await query.answer(results=inline_results, cache_time=30)

    except Exception as e:
        logger.exception(f"Inline search error: {e}")
        await query.answer(
            results=[
                InlineQueryResultArticle(
                    title="⚠️ Error Occurred",
                    description="Something went wrong, try again.",
                    input_message_content=InputTextMessageContent(
                        "⚠️ Something went wrong. Please try again."
                    ),
                )
            ],
            cache_time=0,
        )
