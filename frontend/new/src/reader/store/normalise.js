export const normaliseEntry = apiEntry => {
    return {
        id: apiEntry.id,
        title: apiEntry.title,
        summary: apiEntry.summary,
        posted: apiEntry.date_published,
        content: "",
        feed: normaliseFeed(apiEntry.feed)
    };
};

export const normaliseFeed = apiFeed => {
    return {
        id: apiFeed.id,
        title: apiFeed.title,
        slug: apiFeed.slug,
        unread: apiFeed.unread,
        dateLastScraped: apiFeed.date_last_scraped,
        link: apiFeed.link
    };
}
