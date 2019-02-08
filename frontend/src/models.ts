export interface IFeed {
    title: string;
    link: string;
}

export interface IEntry {
    id: number;
    feed: IFeed;
    title: string;
    link: string;
    content: string;
    summary: string;
    date_published: string;
    states: string[];
}
