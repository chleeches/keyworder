CREATE SCHEMA "keyworder";

CREATE TABLE "keyworder"."articles" (
  "url" varchar PRIMARY KEY,
  "title" varchar,
  "content" varchar,
  "created_at" timestamp
);

CREATE TABLE "keyworder"."title_keywords" (
  "url" varchar,
  "keyword" varchar,
  "count" int,
  PRIMARY KEY ("url", "keyword")
);

CREATE TABLE "keyworder"."content_keywords" (
  "url" varchar,
  "keyword" varchar,
  "count" int,
  PRIMARY KEY ("url", "keyword")
);

ALTER TABLE "keyworder"."title_keywords" ADD FOREIGN KEY ("url") REFERENCES "keyworder"."articles" ("url");
ALTER TABLE "keyworder"."content_keywords" ADD FOREIGN KEY ("url") REFERENCES "keyworder"."articles" ("url");
