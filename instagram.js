const axios = require("axios");

const BASE = "https://graph.facebook.com/v19.0";
const TOKEN = process.env.INSTAGRAM_TOKEN;
const IG_USER_ID = process.env.INSTAGRAM_USER_ID;

async function igGet(path, params = {}) {
  const res = await axios.get(`${BASE}/${path}`, {
    params: { access_token: TOKEN, ...params },
  });
  return res.data;
}

async function getAccountHealth() {
  return igGet(IG_USER_ID, {
    fields: [
      "username",
      "name",
      "biography",
      "followers_count",
      "follows_count",
      "media_count",
      "profile_picture_url",
      "website",
    ].join(","),
  });
}

async function getAccountInsights() {
  const metrics = [
    "accounts_engaged",
    "accounts_reached",
    "impressions",
    "profile_views",
    "total_interactions",
    "website_clicks",
    "follower_count",
  ];

  const [daily, weekly, monthly] = await Promise.all([
    igGet(`${IG_USER_ID}/insights`, {
      metric: metrics.join(","),
      period: "day",
      metric_type: "total_value",
    }),
    igGet(`${IG_USER_ID}/insights`, {
      metric: metrics.join(","),
      period: "week",
      metric_type: "total_value",
    }),
    igGet(`${IG_USER_ID}/insights`, {
      metric: metrics.join(","),
      period: "days_28",
      metric_type: "total_value",
    }),
  ]);

  return { daily: daily.data, weekly: weekly.data, monthly: monthly.data };
}

async function getRecentMedia(limit = 12) {
  const res = await igGet(`${IG_USER_ID}/media`, {
    fields: [
      "id",
      "media_type",
      "media_url",
      "thumbnail_url",
      "caption",
      "timestamp",
      "like_count",
      "comments_count",
      "permalink",
    ].join(","),
    limit,
  });
  return res.data || [];
}

async function getMediaInsights(mediaId, mediaType) {
  const isReel = mediaType === "VIDEO" || mediaType === "REELS";
  const metrics = isReel
    ? [
        "reach",
        "impressions",
        "plays",
        "ig_reels_avg_watch_time",
        "ig_reels_video_view_total_time",
        "total_interactions",
        "comments",
        "likes",
        "saved",
        "shares",
        "follows",
        "profile_visits",
      ]
    : [
        "reach",
        "impressions",
        "total_interactions",
        "comments",
        "likes",
        "saved",
        "shares",
        "follows",
        "profile_visits",
      ];

  try {
    const res = await igGet(`${mediaId}/insights`, {
      metric: metrics.join(","),
    });
    return res.data || [];
  } catch {
    return [];
  }
}

async function getAudienceInsights() {
  const metrics = [
    "follower_demographics",
    "reached_audience_demographics",
    "engaged_audience_demographics",
  ];

  const results = await Promise.allSettled(
    metrics.map((metric) =>
      igGet(`${IG_USER_ID}/insights`, {
        metric,
        period: "lifetime",
        metric_type: "total_value",
        breakdown: "age,gender,country,city",
      })
    )
  );

  return results.reduce((acc, r, i) => {
    acc[metrics[i]] = r.status === "fulfilled" ? r.value.data : null;
    return acc;
  }, {});
}

async function collectFullReport() {
  const [account, accountInsights, media, audience] = await Promise.allSettled([
    getAccountHealth(),
    getAccountInsights(),
    getRecentMedia(12),
    getAudienceInsights(),
  ]);

  const posts = account.status === "fulfilled" && media.status === "fulfilled"
    ? await Promise.all(
        (media.value || []).map(async (post) => {
          const insights = await getMediaInsights(post.id, post.media_type);
          return { ...post, insights };
        })
      )
    : [];

  return {
    account: account.status === "fulfilled" ? account.value : null,
    accountInsights: accountInsights.status === "fulfilled" ? accountInsights.value : null,
    posts,
    audience: audience.status === "fulfilled" ? audience.value : null,
  };
}

module.exports = { collectFullReport };
