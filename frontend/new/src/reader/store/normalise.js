export const normaliseEntry = apiEntry => {
    return {
        id: apiEntry.id,
        title: apiEntry.title,
        summary: apiEntry.summary,
        posted: apiEntry.date_published,
        feed: {
            name: apiEntry.feed.title,
            slug: apiEntry.feed.slug,
            id: apiEntry.feed.id,
            unread: apiEntry.feed.unread
        }
    };
};
