import faker from "faker";

export function createSpoofStory() {
    const feed = createSpoofFeed();
    return {
        id: faker.random.number(),
        title: faker.hacker.phrase(),
        summary: faker.hacker.phrase(),
        posted: "39 minutes ago",
        feed
    };
}

export function createSpoofStories(amount) {
    const spoofStories = [];
    for (let i = 0; i < amount; i++) {
        spoofStories.push(createSpoofStory());
    }
    return spoofStories;
}

export function createSpoofFeed() {
    return {
        id: faker.random.number(),
        name: faker.hacker.abbreviation(),
        slug: faker.lorem.slug(),
        unread: faker.random.number(100)
    };
}

export function createSpoofFeeds(amount) {
    const spoofFeeds = [];
    for (let i = 0; i < amount; i++) {
        spoofFeeds.push(createSpoofFeed());
    }
    return spoofFeeds;
}
