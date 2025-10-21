--
-- PostgreSQL database dump
--

-- Dumped from database version 15.13 (Debian 15.13-1.pgdg120+1)
-- Dumped by pg_dump version 15.13 (Debian 15.13-1.pgdg120+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

ALTER TABLE IF EXISTS ONLY public.solana_users_user_permissions DROP CONSTRAINT IF EXISTS solana_users_user_pe_solanauser_id_d59b0da2_fk_solana_us;
ALTER TABLE IF EXISTS ONLY public.solana_users_user_permissions DROP CONSTRAINT IF EXISTS solana_users_user_pe_permission_id_ba026ff1_fk_auth_perm;
ALTER TABLE IF EXISTS ONLY public.solana_users_groups DROP CONSTRAINT IF EXISTS solana_users_groups_solanauser_id_11c89e39_fk_solana_users_id;
ALTER TABLE IF EXISTS ONLY public.solana_users_groups DROP CONSTRAINT IF EXISTS solana_users_groups_group_id_b1c0d751_fk_auth_group_id;
ALTER TABLE IF EXISTS ONLY public.solana_transactions DROP CONSTRAINT IF EXISTS solana_transactions_user_id_52233802_fk_solana_users_id;
ALTER TABLE IF EXISTS ONLY public.shopping_products DROP CONSTRAINT IF EXISTS shopping_products_category_id_1e3ef60c_fk_shopping_;
ALTER TABLE IF EXISTS ONLY public.shopping_orders DROP CONSTRAINT IF EXISTS shopping_orders_customer_id_39dae0fc_fk_solana_users_id;
ALTER TABLE IF EXISTS ONLY public.shopping_order_items DROP CONSTRAINT IF EXISTS shopping_order_items_product_id_79be391b_fk_shopping_;
ALTER TABLE IF EXISTS ONLY public.shopping_order_items DROP CONSTRAINT IF EXISTS shopping_order_items_order_id_36d4448b_fk_shopping_orders_id;
ALTER TABLE IF EXISTS ONLY public.rwa_assets DROP CONSTRAINT IF EXISTS rwa_assets_category_id_61d8811d_fk_rwa_categories_id;
ALTER TABLE IF EXISTS ONLY public.investments DROP CONSTRAINT IF EXISTS investments_rwa_asset_id_09fe90d8_fk_rwa_assets_id;
ALTER TABLE IF EXISTS ONLY public.investments DROP CONSTRAINT IF EXISTS investments_investor_id_96559232_fk_solana_users_id;
ALTER TABLE IF EXISTS ONLY public.grade_permissions DROP CONSTRAINT IF EXISTS grade_permissions_permission_id_f2072039_fk_admin_per;
ALTER TABLE IF EXISTS ONLY public.grade_permissions DROP CONSTRAINT IF EXISTS grade_permissions_grade_id_59c9bf2e_fk_admin_grades_id;
ALTER TABLE IF EXISTS ONLY public.face_verifications DROP CONSTRAINT IF EXISTS face_verifications_user_id_e72defbc_fk_solana_users_id;
ALTER TABLE IF EXISTS ONLY public.django_admin_log DROP CONSTRAINT IF EXISTS django_admin_log_user_id_c564eba6_fk_solana_users_id;
ALTER TABLE IF EXISTS ONLY public.django_admin_log DROP CONSTRAINT IF EXISTS django_admin_log_content_type_id_c4bce8eb_fk_django_co;
ALTER TABLE IF EXISTS ONLY public.auth_permission DROP CONSTRAINT IF EXISTS auth_permission_content_type_id_2f476e4b_fk_django_co;
ALTER TABLE IF EXISTS ONLY public.auth_group_permissions DROP CONSTRAINT IF EXISTS auth_group_permissions_group_id_b120cbf9_fk_auth_group_id;
ALTER TABLE IF EXISTS ONLY public.auth_group_permissions DROP CONSTRAINT IF EXISTS auth_group_permissio_permission_id_84c5c92e_fk_auth_perm;
ALTER TABLE IF EXISTS ONLY public.admin_users DROP CONSTRAINT IF EXISTS admin_users_user_id_5db507a7_fk_solana_users_id;
ALTER TABLE IF EXISTS ONLY public.admin_users DROP CONSTRAINT IF EXISTS admin_users_grade_id_d7e8ab63_fk_admin_grades_id;
DROP INDEX IF EXISTS public.token_ecosy_order_643813_idx;
DROP INDEX IF EXISTS public.team_member_order_a5326a_idx;
DROP INDEX IF EXISTS public.strategy_ph_order_bc8c62_idx;
DROP INDEX IF EXISTS public.solana_users_wallet_address_49950d1a_like;
DROP INDEX IF EXISTS public.solana_users_username_02a6e338_like;
DROP INDEX IF EXISTS public.solana_users_user_permissions_solanauser_id_d59b0da2;
DROP INDEX IF EXISTS public.solana_users_user_permissions_permission_id_ba026ff1;
DROP INDEX IF EXISTS public.solana_users_groups_solanauser_id_11c89e39;
DROP INDEX IF EXISTS public.solana_users_groups_group_id_b1c0d751;
DROP INDEX IF EXISTS public.solana_transactions_user_id_52233802;
DROP INDEX IF EXISTS public.solana_transactions_transaction_hash_045f83c1_like;
DROP INDEX IF EXISTS public.shopping_products_category_id_1e3ef60c;
DROP INDEX IF EXISTS public.shopping_pr_product_75ea01_idx;
DROP INDEX IF EXISTS public.shopping_pr_is_feat_450291_idx;
DROP INDEX IF EXISTS public.shopping_pr_categor_c946bf_idx;
DROP INDEX IF EXISTS public.shopping_orders_order_number_bf3d25d1_like;
DROP INDEX IF EXISTS public.shopping_orders_customer_id_39dae0fc;
DROP INDEX IF EXISTS public.shopping_order_items_product_id_79be391b;
DROP INDEX IF EXISTS public.shopping_order_items_order_id_36d4448b;
DROP INDEX IF EXISTS public.shopping_or_order_n_0ddc42_idx;
DROP INDEX IF EXISTS public.shopping_or_custome_66824e_idx;
DROP INDEX IF EXISTS public.shopping_or_created_912a6b_idx;
DROP INDEX IF EXISTS public.shopping_categories_order_38dadc9d;
DROP INDEX IF EXISTS public.shopping_categories_name_87272f6e_like;
DROP INDEX IF EXISTS public.rwa_categories_order_645aea7b;
DROP INDEX IF EXISTS public.rwa_categories_name_bbbe843c_like;
DROP INDEX IF EXISTS public.rwa_assets_risk_le_4b272a_idx;
DROP INDEX IF EXISTS public.rwa_assets_is_feat_a378f2_idx;
DROP INDEX IF EXISTS public.rwa_assets_category_id_61d8811d;
DROP INDEX IF EXISTS public.rwa_assets_categor_ed240e_idx;
DROP INDEX IF EXISTS public.project_fea_order_fc4473_idx;
DROP INDEX IF EXISTS public.investments_rwa_asset_id_09fe90d8;
DROP INDEX IF EXISTS public.investments_rwa_ass_c871e4_idx;
DROP INDEX IF EXISTS public.investments_investor_id_96559232;
DROP INDEX IF EXISTS public.investments_investo_49ded7_idx;
DROP INDEX IF EXISTS public.investments_investm_d1de42_idx;
DROP INDEX IF EXISTS public.grade_permissions_permission_id_f2072039;
DROP INDEX IF EXISTS public.grade_permissions_grade_id_59c9bf2e;
DROP INDEX IF EXISTS public.face_verifications_user_id_e72defbc;
DROP INDEX IF EXISTS public.face_verifi_verifie_9737b6_idx;
DROP INDEX IF EXISTS public.face_verifi_user_id_d95bf7_idx;
DROP INDEX IF EXISTS public.django_session_session_key_c0390e0f_like;
DROP INDEX IF EXISTS public.django_session_expire_date_a5c62663;
DROP INDEX IF EXISTS public.django_admin_log_user_id_c564eba6;
DROP INDEX IF EXISTS public.django_admin_log_content_type_id_c4bce8eb;
DROP INDEX IF EXISTS public.development_order_7b87e9_idx;
DROP INDEX IF EXISTS public.business_contents_section_8db8dcc8_like;
DROP INDEX IF EXISTS public.business_contents_section_8db8dcc8;
DROP INDEX IF EXISTS public.business_contents_order_e9a2ea4e;
DROP INDEX IF EXISTS public.auth_permission_content_type_id_2f476e4b;
DROP INDEX IF EXISTS public.auth_nonces_wallet_address_67e2508a_like;
DROP INDEX IF EXISTS public.auth_nonces_wallet_address_67e2508a;
DROP INDEX IF EXISTS public.auth_nonces_nonce_ea70b2b7_like;
DROP INDEX IF EXISTS public.auth_group_permissions_permission_id_84c5c92e;
DROP INDEX IF EXISTS public.auth_group_permissions_group_id_b120cbf9;
DROP INDEX IF EXISTS public.auth_group_name_a6ea08ec_like;
DROP INDEX IF EXISTS public.admin_users_grade_id_d7e8ab63;
DROP INDEX IF EXISTS public.admin_permissions_name_01494afb_like;
DROP INDEX IF EXISTS public.admin_permissions_codename_41bf9c7e_like;
DROP INDEX IF EXISTS public.admin_grades_name_8af46b3c_like;
ALTER TABLE IF EXISTS ONLY public.token_ecosystems DROP CONSTRAINT IF EXISTS token_ecosystems_pkey;
ALTER TABLE IF EXISTS ONLY public.team_members DROP CONSTRAINT IF EXISTS team_members_pkey;
ALTER TABLE IF EXISTS ONLY public.strategy_phases DROP CONSTRAINT IF EXISTS strategy_phases_pkey;
ALTER TABLE IF EXISTS ONLY public.solana_users DROP CONSTRAINT IF EXISTS solana_users_wallet_address_key;
ALTER TABLE IF EXISTS ONLY public.solana_users DROP CONSTRAINT IF EXISTS solana_users_username_key;
ALTER TABLE IF EXISTS ONLY public.solana_users_user_permissions DROP CONSTRAINT IF EXISTS solana_users_user_permissions_pkey;
ALTER TABLE IF EXISTS ONLY public.solana_users_user_permissions DROP CONSTRAINT IF EXISTS solana_users_user_permis_solanauser_id_permission_75f6ca92_uniq;
ALTER TABLE IF EXISTS ONLY public.solana_users DROP CONSTRAINT IF EXISTS solana_users_pkey;
ALTER TABLE IF EXISTS ONLY public.solana_users_groups DROP CONSTRAINT IF EXISTS solana_users_groups_solanauser_id_group_id_bf859b19_uniq;
ALTER TABLE IF EXISTS ONLY public.solana_users_groups DROP CONSTRAINT IF EXISTS solana_users_groups_pkey;
ALTER TABLE IF EXISTS ONLY public.solana_transactions DROP CONSTRAINT IF EXISTS solana_transactions_transaction_hash_key;
ALTER TABLE IF EXISTS ONLY public.solana_transactions DROP CONSTRAINT IF EXISTS solana_transactions_pkey;
ALTER TABLE IF EXISTS ONLY public.shopping_products DROP CONSTRAINT IF EXISTS shopping_products_pkey;
ALTER TABLE IF EXISTS ONLY public.shopping_orders DROP CONSTRAINT IF EXISTS shopping_orders_pkey;
ALTER TABLE IF EXISTS ONLY public.shopping_orders DROP CONSTRAINT IF EXISTS shopping_orders_order_number_key;
ALTER TABLE IF EXISTS ONLY public.shopping_order_items DROP CONSTRAINT IF EXISTS shopping_order_items_pkey;
ALTER TABLE IF EXISTS ONLY public.shopping_categories DROP CONSTRAINT IF EXISTS shopping_categories_pkey;
ALTER TABLE IF EXISTS ONLY public.shopping_categories DROP CONSTRAINT IF EXISTS shopping_categories_name_key;
ALTER TABLE IF EXISTS ONLY public.rwa_categories DROP CONSTRAINT IF EXISTS rwa_categories_pkey;
ALTER TABLE IF EXISTS ONLY public.rwa_categories DROP CONSTRAINT IF EXISTS rwa_categories_name_key;
ALTER TABLE IF EXISTS ONLY public.rwa_assets DROP CONSTRAINT IF EXISTS rwa_assets_pkey;
ALTER TABLE IF EXISTS ONLY public.project_features DROP CONSTRAINT IF EXISTS project_features_pkey;
ALTER TABLE IF EXISTS ONLY public.investments DROP CONSTRAINT IF EXISTS investments_pkey;
ALTER TABLE IF EXISTS ONLY public.grade_permissions DROP CONSTRAINT IF EXISTS grade_permissions_pkey;
ALTER TABLE IF EXISTS ONLY public.grade_permissions DROP CONSTRAINT IF EXISTS grade_permissions_grade_id_permission_id_7b6d0f61_uniq;
ALTER TABLE IF EXISTS ONLY public.face_verifications DROP CONSTRAINT IF EXISTS face_verifications_pkey;
ALTER TABLE IF EXISTS ONLY public.django_session DROP CONSTRAINT IF EXISTS django_session_pkey;
ALTER TABLE IF EXISTS ONLY public.django_migrations DROP CONSTRAINT IF EXISTS django_migrations_pkey;
ALTER TABLE IF EXISTS ONLY public.django_content_type DROP CONSTRAINT IF EXISTS django_content_type_pkey;
ALTER TABLE IF EXISTS ONLY public.django_content_type DROP CONSTRAINT IF EXISTS django_content_type_app_label_model_76bd3d3b_uniq;
ALTER TABLE IF EXISTS ONLY public.django_admin_log DROP CONSTRAINT IF EXISTS django_admin_log_pkey;
ALTER TABLE IF EXISTS ONLY public.development_timelines DROP CONSTRAINT IF EXISTS development_timelines_pkey;
ALTER TABLE IF EXISTS ONLY public.business_contents DROP CONSTRAINT IF EXISTS business_contents_section_order_5ecbff5d_uniq;
ALTER TABLE IF EXISTS ONLY public.business_contents DROP CONSTRAINT IF EXISTS business_contents_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_permission DROP CONSTRAINT IF EXISTS auth_permission_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_permission DROP CONSTRAINT IF EXISTS auth_permission_content_type_id_codename_01ab375a_uniq;
ALTER TABLE IF EXISTS ONLY public.auth_nonces DROP CONSTRAINT IF EXISTS auth_nonces_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_nonces DROP CONSTRAINT IF EXISTS auth_nonces_nonce_key;
ALTER TABLE IF EXISTS ONLY public.auth_group DROP CONSTRAINT IF EXISTS auth_group_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_group_permissions DROP CONSTRAINT IF EXISTS auth_group_permissions_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_group_permissions DROP CONSTRAINT IF EXISTS auth_group_permissions_group_id_permission_id_0cd325b0_uniq;
ALTER TABLE IF EXISTS ONLY public.auth_group DROP CONSTRAINT IF EXISTS auth_group_name_key;
ALTER TABLE IF EXISTS ONLY public.admin_users DROP CONSTRAINT IF EXISTS admin_users_user_id_key;
ALTER TABLE IF EXISTS ONLY public.admin_users DROP CONSTRAINT IF EXISTS admin_users_pkey;
ALTER TABLE IF EXISTS ONLY public.admin_permissions DROP CONSTRAINT IF EXISTS admin_permissions_pkey;
ALTER TABLE IF EXISTS ONLY public.admin_permissions DROP CONSTRAINT IF EXISTS admin_permissions_name_key;
ALTER TABLE IF EXISTS ONLY public.admin_permissions DROP CONSTRAINT IF EXISTS admin_permissions_codename_key;
ALTER TABLE IF EXISTS ONLY public.admin_grades DROP CONSTRAINT IF EXISTS admin_grades_pkey;
ALTER TABLE IF EXISTS ONLY public.admin_grades DROP CONSTRAINT IF EXISTS admin_grades_name_key;
DROP TABLE IF EXISTS public.token_ecosystems;
DROP TABLE IF EXISTS public.team_members;
DROP TABLE IF EXISTS public.strategy_phases;
DROP TABLE IF EXISTS public.solana_users_user_permissions;
DROP TABLE IF EXISTS public.solana_users_groups;
DROP TABLE IF EXISTS public.solana_users;
DROP TABLE IF EXISTS public.solana_transactions;
DROP TABLE IF EXISTS public.shopping_products;
DROP TABLE IF EXISTS public.shopping_orders;
DROP TABLE IF EXISTS public.shopping_order_items;
DROP TABLE IF EXISTS public.shopping_categories;
DROP TABLE IF EXISTS public.rwa_categories;
DROP TABLE IF EXISTS public.rwa_assets;
DROP TABLE IF EXISTS public.project_features;
DROP TABLE IF EXISTS public.investments;
DROP TABLE IF EXISTS public.grade_permissions;
DROP TABLE IF EXISTS public.face_verifications;
DROP TABLE IF EXISTS public.django_session;
DROP TABLE IF EXISTS public.django_migrations;
DROP TABLE IF EXISTS public.django_content_type;
DROP TABLE IF EXISTS public.django_admin_log;
DROP TABLE IF EXISTS public.development_timelines;
DROP TABLE IF EXISTS public.business_contents;
DROP TABLE IF EXISTS public.auth_permission;
DROP TABLE IF EXISTS public.auth_nonces;
DROP TABLE IF EXISTS public.auth_group_permissions;
DROP TABLE IF EXISTS public.auth_group;
DROP TABLE IF EXISTS public.admin_users;
DROP TABLE IF EXISTS public.admin_permissions;
DROP TABLE IF EXISTS public.admin_grades;
SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: admin_grades; Type: TABLE; Schema: public; Owner: gli
--

CREATE TABLE public.admin_grades (
    id bigint NOT NULL,
    name character varying(50) NOT NULL,
    description text,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL
);


ALTER TABLE public.admin_grades OWNER TO gli;

--
-- Name: admin_grades_id_seq; Type: SEQUENCE; Schema: public; Owner: gli
--

ALTER TABLE public.admin_grades ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.admin_grades_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: admin_permissions; Type: TABLE; Schema: public; Owner: gli
--

CREATE TABLE public.admin_permissions (
    id bigint NOT NULL,
    name character varying(100) NOT NULL,
    codename character varying(100) NOT NULL,
    description text,
    created_at timestamp with time zone NOT NULL
);


ALTER TABLE public.admin_permissions OWNER TO gli;

--
-- Name: admin_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: gli
--

ALTER TABLE public.admin_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.admin_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: admin_users; Type: TABLE; Schema: public; Owner: gli
--

CREATE TABLE public.admin_users (
    id bigint NOT NULL,
    is_active boolean NOT NULL,
    last_login_ip inet,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    grade_id bigint NOT NULL,
    user_id uuid NOT NULL
);


ALTER TABLE public.admin_users OWNER TO gli;

--
-- Name: admin_users_id_seq; Type: SEQUENCE; Schema: public; Owner: gli
--

ALTER TABLE public.admin_users ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.admin_users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: gli
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO gli;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: gli
--

ALTER TABLE public.auth_group ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: gli
--

CREATE TABLE public.auth_group_permissions (
    id bigint NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO gli;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: gli
--

ALTER TABLE public.auth_group_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_nonces; Type: TABLE; Schema: public; Owner: gli
--

CREATE TABLE public.auth_nonces (
    id bigint NOT NULL,
    wallet_address character varying(50) NOT NULL,
    nonce character varying(64) NOT NULL,
    created_at timestamp with time zone NOT NULL,
    used boolean NOT NULL
);


ALTER TABLE public.auth_nonces OWNER TO gli;

--
-- Name: auth_nonces_id_seq; Type: SEQUENCE; Schema: public; Owner: gli
--

ALTER TABLE public.auth_nonces ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_nonces_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: gli
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO gli;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: gli
--

ALTER TABLE public.auth_permission ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: business_contents; Type: TABLE; Schema: public; Owner: gli
--

CREATE TABLE public.business_contents (
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    section character varying(20) NOT NULL,
    title character varying(200) NOT NULL,
    subtitle character varying(300) NOT NULL,
    content text NOT NULL,
    image_url character varying(200),
    "order" integer NOT NULL,
    status character varying(20) NOT NULL,
    meta_data jsonb NOT NULL,
    CONSTRAINT business_contents_order_check CHECK (("order" >= 0))
);


ALTER TABLE public.business_contents OWNER TO gli;

--
-- Name: development_timelines; Type: TABLE; Schema: public; Owner: gli
--

CREATE TABLE public.development_timelines (
    id uuid NOT NULL,
    quarter character varying(20) NOT NULL,
    status_icon character varying(10) NOT NULL,
    title_ko character varying(200) NOT NULL,
    title_en character varying(200) NOT NULL,
    description_ko text NOT NULL,
    description_en text NOT NULL,
    "order" integer NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL
);


ALTER TABLE public.development_timelines OWNER TO gli;

--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: gli
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id uuid NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO gli;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: gli
--

ALTER TABLE public.django_admin_log ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: gli
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO gli;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: gli
--

ALTER TABLE public.django_content_type ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: gli
--

CREATE TABLE public.django_migrations (
    id bigint NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO gli;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: gli
--

ALTER TABLE public.django_migrations ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: gli
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO gli;

--
-- Name: face_verifications; Type: TABLE; Schema: public; Owner: gli
--

CREATE TABLE public.face_verifications (
    id uuid NOT NULL,
    verified boolean NOT NULL,
    confidence numeric(5,4) NOT NULL,
    liveness_score numeric(5,4) NOT NULL,
    attempts integer NOT NULL,
    check_details jsonb,
    verification_timestamp timestamp with time zone NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    user_id uuid NOT NULL
);


ALTER TABLE public.face_verifications OWNER TO gli;

--
-- Name: grade_permissions; Type: TABLE; Schema: public; Owner: gli
--

CREATE TABLE public.grade_permissions (
    id bigint NOT NULL,
    created_at timestamp with time zone NOT NULL,
    grade_id bigint NOT NULL,
    permission_id bigint NOT NULL
);


ALTER TABLE public.grade_permissions OWNER TO gli;

--
-- Name: grade_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: gli
--

ALTER TABLE public.grade_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.grade_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: investments; Type: TABLE; Schema: public; Owner: gli
--

CREATE TABLE public.investments (
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    amount_glib numeric(20,8) NOT NULL,
    amount_usd_at_time numeric(15,2) NOT NULL,
    investment_date timestamp with time zone NOT NULL,
    expected_return_date timestamp with time zone NOT NULL,
    lock_end_date timestamp with time zone,
    expected_apy_at_time numeric(5,2) NOT NULL,
    current_value_glib numeric(20,8) NOT NULL,
    realized_profit_glib numeric(20,8) NOT NULL,
    status character varying(20) NOT NULL,
    investment_tx_hash character varying(100) NOT NULL,
    withdrawal_tx_hash character varying(100) NOT NULL,
    metadata jsonb NOT NULL,
    investor_id uuid NOT NULL,
    rwa_asset_id uuid NOT NULL
);


ALTER TABLE public.investments OWNER TO gli;

--
-- Name: project_features; Type: TABLE; Schema: public; Owner: gli
--

CREATE TABLE public.project_features (
    id uuid NOT NULL,
    icon character varying(10) NOT NULL,
    title_ko character varying(200) NOT NULL,
    title_en character varying(200) NOT NULL,
    description_ko text NOT NULL,
    description_en text NOT NULL,
    "order" integer NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL
);


ALTER TABLE public.project_features OWNER TO gli;

--
-- Name: rwa_assets; Type: TABLE; Schema: public; Owner: gli
--

CREATE TABLE public.rwa_assets (
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    name character varying(200) NOT NULL,
    description text NOT NULL,
    short_description character varying(500) NOT NULL,
    total_value_usd numeric(15,2) NOT NULL,
    min_investment_glib numeric(20,8) NOT NULL,
    max_investment_glib numeric(20,8),
    expected_apy numeric(5,2) NOT NULL,
    historical_returns jsonb NOT NULL,
    risk_level character varying(20) NOT NULL,
    risk_factors jsonb NOT NULL,
    investment_period_months integer NOT NULL,
    lock_period_months integer NOT NULL,
    asset_location character varying(200) NOT NULL,
    asset_type character varying(100) NOT NULL,
    underlying_assets jsonb NOT NULL,
    main_image_url character varying(200) NOT NULL,
    image_urls jsonb NOT NULL,
    document_urls jsonb NOT NULL,
    total_invested_glib numeric(20,8) NOT NULL,
    investor_count integer NOT NULL,
    funding_target_glib numeric(20,8),
    status character varying(20) NOT NULL,
    is_featured boolean NOT NULL,
    metadata jsonb NOT NULL,
    category_id uuid NOT NULL,
    area_sqm numeric(10,2),
    asset_location_en character varying(200) NOT NULL,
    asset_type_en character varying(100) NOT NULL,
    description_en text NOT NULL,
    name_en character varying(200) NOT NULL,
    operation_type character varying(20) NOT NULL,
    short_description_en character varying(500) NOT NULL,
    CONSTRAINT rwa_assets_investment_period_months_check CHECK ((investment_period_months >= 0)),
    CONSTRAINT rwa_assets_investor_count_check CHECK ((investor_count >= 0)),
    CONSTRAINT rwa_assets_lock_period_months_check CHECK ((lock_period_months >= 0))
);


ALTER TABLE public.rwa_assets OWNER TO gli;

--
-- Name: rwa_categories; Type: TABLE; Schema: public; Owner: gli
--

CREATE TABLE public.rwa_categories (
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    name character varying(100) NOT NULL,
    description text NOT NULL,
    icon character varying(100) NOT NULL,
    "order" integer NOT NULL,
    is_active boolean NOT NULL,
    CONSTRAINT rwa_categories_order_check CHECK (("order" >= 0))
);


ALTER TABLE public.rwa_categories OWNER TO gli;

--
-- Name: shopping_categories; Type: TABLE; Schema: public; Owner: gli
--

CREATE TABLE public.shopping_categories (
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    name character varying(100) NOT NULL,
    description text NOT NULL,
    icon character varying(100) NOT NULL,
    "order" integer NOT NULL,
    is_active boolean NOT NULL,
    description_en text NOT NULL,
    name_en character varying(100) NOT NULL,
    CONSTRAINT shopping_categories_order_check CHECK (("order" >= 0))
);


ALTER TABLE public.shopping_categories OWNER TO gli;

--
-- Name: shopping_order_items; Type: TABLE; Schema: public; Owner: gli
--

CREATE TABLE public.shopping_order_items (
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    product_name character varying(200) NOT NULL,
    product_price_glil numeric(20,8) NOT NULL,
    quantity integer NOT NULL,
    selected_attributes jsonb NOT NULL,
    order_id uuid NOT NULL,
    product_id uuid NOT NULL,
    CONSTRAINT shopping_order_items_quantity_check CHECK ((quantity >= 0))
);


ALTER TABLE public.shopping_order_items OWNER TO gli;

--
-- Name: shopping_orders; Type: TABLE; Schema: public; Owner: gli
--

CREATE TABLE public.shopping_orders (
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    order_number character varying(50) NOT NULL,
    total_amount_glil numeric(20,8) NOT NULL,
    total_amount_usd numeric(10,2),
    status character varying(20) NOT NULL,
    payment_tx_hash character varying(100) NOT NULL,
    paid_at timestamp with time zone,
    shipping_address jsonb NOT NULL,
    tracking_number character varying(100) NOT NULL,
    shipped_at timestamp with time zone,
    delivered_at timestamp with time zone,
    notes text NOT NULL,
    metadata jsonb NOT NULL,
    customer_id uuid NOT NULL
);


ALTER TABLE public.shopping_orders OWNER TO gli;

--
-- Name: shopping_products; Type: TABLE; Schema: public; Owner: gli
--

CREATE TABLE public.shopping_products (
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    name character varying(200) NOT NULL,
    description text NOT NULL,
    short_description character varying(500) NOT NULL,
    product_type character varying(20) NOT NULL,
    price_glil numeric(20,8) NOT NULL,
    price_usd numeric(10,2),
    stock_quantity integer NOT NULL,
    unlimited_stock boolean NOT NULL,
    main_image_url character varying(200) NOT NULL,
    image_urls jsonb NOT NULL,
    status character varying(20) NOT NULL,
    is_featured boolean NOT NULL,
    tags jsonb NOT NULL,
    attributes jsonb NOT NULL,
    view_count integer NOT NULL,
    purchase_count integer NOT NULL,
    category_id uuid NOT NULL,
    description_en text NOT NULL,
    name_en character varying(200) NOT NULL,
    short_description_en character varying(500) NOT NULL,
    CONSTRAINT shopping_products_purchase_count_check CHECK ((purchase_count >= 0)),
    CONSTRAINT shopping_products_stock_quantity_check CHECK ((stock_quantity >= 0)),
    CONSTRAINT shopping_products_view_count_check CHECK ((view_count >= 0))
);


ALTER TABLE public.shopping_products OWNER TO gli;

--
-- Name: solana_transactions; Type: TABLE; Schema: public; Owner: gli
--

CREATE TABLE public.solana_transactions (
    id bigint NOT NULL,
    transaction_hash character varying(100) NOT NULL,
    transaction_type character varying(20) NOT NULL,
    amount numeric(20,9) NOT NULL,
    status character varying(20) NOT NULL,
    created_at timestamp with time zone NOT NULL,
    confirmed_at timestamp with time zone,
    user_id uuid NOT NULL
);


ALTER TABLE public.solana_transactions OWNER TO gli;

--
-- Name: solana_transactions_id_seq; Type: SEQUENCE; Schema: public; Owner: gli
--

ALTER TABLE public.solana_transactions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.solana_transactions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: solana_users; Type: TABLE; Schema: public; Owner: gli
--

CREATE TABLE public.solana_users (
    password character varying(128) NOT NULL,
    is_superuser boolean NOT NULL,
    is_staff boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    wallet_address character varying(50),
    username character varying(100) NOT NULL,
    email character varying(254),
    first_name character varying(50) NOT NULL,
    last_name character varying(50) NOT NULL,
    membership_level character varying(20) NOT NULL,
    sol_balance numeric(20,9) NOT NULL,
    last_balance_update timestamp with time zone NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    last_login timestamp with time zone,
    vpx_experience integer NOT NULL,
    vpx_partner integer NOT NULL,
    vpx_verify integer NOT NULL
);


ALTER TABLE public.solana_users OWNER TO gli;

--
-- Name: solana_users_groups; Type: TABLE; Schema: public; Owner: gli
--

CREATE TABLE public.solana_users_groups (
    id bigint NOT NULL,
    solanauser_id uuid NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.solana_users_groups OWNER TO gli;

--
-- Name: solana_users_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: gli
--

ALTER TABLE public.solana_users_groups ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.solana_users_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: solana_users_user_permissions; Type: TABLE; Schema: public; Owner: gli
--

CREATE TABLE public.solana_users_user_permissions (
    id bigint NOT NULL,
    solanauser_id uuid NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.solana_users_user_permissions OWNER TO gli;

--
-- Name: solana_users_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: gli
--

ALTER TABLE public.solana_users_user_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.solana_users_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: strategy_phases; Type: TABLE; Schema: public; Owner: gli
--

CREATE TABLE public.strategy_phases (
    id uuid NOT NULL,
    icon character varying(10) NOT NULL,
    title_ko character varying(200) NOT NULL,
    title_en character varying(200) NOT NULL,
    description_ko text NOT NULL,
    description_en text NOT NULL,
    features_ko jsonb NOT NULL,
    "order" integer NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    features_en jsonb DEFAULT '[]'::jsonb NOT NULL
);


ALTER TABLE public.strategy_phases OWNER TO gli;

--
-- Name: team_members; Type: TABLE; Schema: public; Owner: gli
--

CREATE TABLE public.team_members (
    id uuid NOT NULL,
    image_url character varying(500),
    position_ko character varying(100) NOT NULL,
    position_en character varying(100) NOT NULL,
    role_ko text NOT NULL,
    role_en text NOT NULL,
    tags jsonb NOT NULL,
    "order" integer NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    name_en character varying(50) NOT NULL,
    name_ko character varying(50) NOT NULL
);


ALTER TABLE public.team_members OWNER TO gli;

--
-- Name: token_ecosystems; Type: TABLE; Schema: public; Owner: gli
--

CREATE TABLE public.token_ecosystems (
    id uuid NOT NULL,
    icon character varying(10) NOT NULL,
    name character varying(100) NOT NULL,
    symbol character varying(20) NOT NULL,
    description_ko text NOT NULL,
    description_en text NOT NULL,
    total_supply character varying(100) NOT NULL,
    current_price character varying(50) NOT NULL,
    "order" integer NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    features_en jsonb NOT NULL,
    features_ko jsonb NOT NULL
);


ALTER TABLE public.token_ecosystems OWNER TO gli;

--
-- Data for Name: admin_grades; Type: TABLE DATA; Schema: public; Owner: gli
--

COPY public.admin_grades (id, name, description, created_at, updated_at) FROM stdin;
1	슈퍼 관리자	모든 권한을 가진 최고 관리자	2025-10-14 00:11:17.729+09	2025-10-14 00:11:17.729+09
2	일반 관리자	제한된 권한을 가진 일반 관리자	2025-10-14 00:11:17.737+09	2025-10-14 00:11:17.737+09
\.


--
-- Data for Name: admin_permissions; Type: TABLE DATA; Schema: public; Owner: gli
--

COPY public.admin_permissions (id, name, codename, description, created_at) FROM stdin;
\.


--
-- Data for Name: admin_users; Type: TABLE DATA; Schema: public; Owner: gli
--

COPY public.admin_users (id, is_active, last_login_ip, created_at, updated_at, grade_id, user_id) FROM stdin;
1	t	\N	2025-10-14 00:11:17.757+09	2025-10-14 00:11:17.757+09	2	b50c4ed5-c11f-41fc-966f-83d0736683d1
2	t	\N	2025-10-14 00:11:17.767+09	2025-10-14 00:11:17.768+09	1	7d6c5a92-d357-45a6-a533-6eb47c3af5d7
3	t	\N	2025-10-14 00:11:17.778+09	2025-10-14 00:11:17.778+09	1	6da4715f-dee9-4821-8c39-6310f46250b3
4	t	\N	2025-10-14 00:11:17.787+09	2025-10-14 00:11:17.787+09	2	513bd8bd-bfdd-4c41-9062-06a93beec771
5	t	\N	2025-10-14 00:11:17.796+09	2025-10-14 00:11:17.796+09	1	2dd24951-db0a-49b7-9dcb-47f06a366fca
6	t	\N	2025-10-14 00:11:17.805+09	2025-10-14 00:11:17.805+09	2	25b34ad5-ddc0-41bc-a35d-2c3de28e22c9
7	t	\N	2025-10-14 00:11:17.815+09	2025-10-14 00:11:17.815+09	1	03129597-8698-473b-bc65-9569b04b856f
\.


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: gli
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: gli
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_nonces; Type: TABLE DATA; Schema: public; Owner: gli
--

COPY public.auth_nonces (id, wallet_address, nonce, created_at, used) FROM stdin;
1	5rFHPQ62n6f7dTJRwvuEzjLrvgYtRyfuimnnnm7FTug6	99be559b46ecc66d0b18320de8f04076fe0c15af957cae08d12437b47fef79ba	2025-10-14 13:09:41.263+09	t
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: gli
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add permission	1	add_permission
2	Can change permission	1	change_permission
3	Can delete permission	1	delete_permission
4	Can view permission	1	view_permission
5	Can add group	2	add_group
6	Can change group	2	change_group
7	Can delete group	2	delete_group
8	Can view group	2	view_group
9	Can add content type	3	add_contenttype
10	Can change content type	3	change_contenttype
11	Can delete content type	3	delete_contenttype
12	Can view content type	3	view_contenttype
13	Can add auth nonce	4	add_authnonce
14	Can change auth nonce	4	change_authnonce
15	Can delete auth nonce	4	delete_authnonce
16	Can view auth nonce	4	view_authnonce
17	Can add solana user	5	add_solanauser
18	Can change solana user	5	change_solanauser
19	Can delete solana user	5	delete_solanauser
20	Can view solana user	5	view_solanauser
21	Can add solana transaction	6	add_solanatransaction
22	Can change solana transaction	6	change_solanatransaction
23	Can delete solana transaction	6	delete_solanatransaction
24	Can view solana transaction	6	view_solanatransaction
25	Can add face verification	7	add_faceverification
26	Can change face verification	7	change_faceverification
27	Can delete face verification	7	delete_faceverification
28	Can view face verification	7	view_faceverification
29	Can add admin grade	8	add_admingrade
30	Can change admin grade	8	change_admingrade
31	Can delete admin grade	8	delete_admingrade
32	Can view admin grade	8	view_admingrade
33	Can add admin permission	9	add_adminpermission
34	Can change admin permission	9	change_adminpermission
35	Can delete admin permission	9	delete_adminpermission
36	Can view admin permission	9	view_adminpermission
37	Can add admin user	10	add_adminuser
38	Can change admin user	10	change_adminuser
39	Can delete admin user	10	delete_adminuser
40	Can view admin user	10	view_adminuser
41	Can add grade permission	11	add_gradepermission
42	Can change grade permission	11	change_gradepermission
43	Can delete grade permission	11	delete_gradepermission
44	Can view grade permission	11	view_gradepermission
45	Can add team member	12	add_teammember
46	Can change team member	12	change_teammember
47	Can delete team member	12	delete_teammember
48	Can view team member	12	view_teammember
49	Can add project feature	13	add_projectfeature
50	Can change project feature	13	change_projectfeature
51	Can delete project feature	13	delete_projectfeature
52	Can view project feature	13	view_projectfeature
53	Can add strategy phase	14	add_strategyphase
54	Can change strategy phase	14	change_strategyphase
55	Can delete strategy phase	14	delete_strategyphase
56	Can view strategy phase	14	view_strategyphase
57	Can add development timeline	15	add_developmenttimeline
58	Can change development timeline	15	change_developmenttimeline
59	Can delete development timeline	15	delete_developmenttimeline
60	Can view development timeline	15	view_developmenttimeline
61	Can add token ecosystem	16	add_tokenecosystem
62	Can change token ecosystem	16	change_tokenecosystem
63	Can delete token ecosystem	16	delete_tokenecosystem
64	Can view token ecosystem	16	view_tokenecosystem
65	Can add rwa category	17	add_rwacategory
66	Can change rwa category	17	change_rwacategory
67	Can delete rwa category	17	delete_rwacategory
68	Can view rwa category	17	view_rwacategory
69	Can add shopping category	18	add_shoppingcategory
70	Can change shopping category	18	change_shoppingcategory
71	Can delete shopping category	18	delete_shoppingcategory
72	Can view shopping category	18	view_shoppingcategory
73	Can add business content	19	add_businesscontent
74	Can change business content	19	change_businesscontent
75	Can delete business content	19	delete_businesscontent
76	Can view business content	19	view_businesscontent
77	Can add rwa asset	20	add_rwaasset
78	Can change rwa asset	20	change_rwaasset
79	Can delete rwa asset	20	delete_rwaasset
80	Can view rwa asset	20	view_rwaasset
81	Can add shopping order	21	add_shoppingorder
82	Can change shopping order	21	change_shoppingorder
83	Can delete shopping order	21	delete_shoppingorder
84	Can view shopping order	21	view_shoppingorder
85	Can add shopping product	22	add_shoppingproduct
86	Can change shopping product	22	change_shoppingproduct
87	Can delete shopping product	22	delete_shoppingproduct
88	Can view shopping product	22	view_shoppingproduct
89	Can add shopping order item	23	add_shoppingorderitem
90	Can change shopping order item	23	change_shoppingorderitem
91	Can delete shopping order item	23	delete_shoppingorderitem
92	Can view shopping order item	23	view_shoppingorderitem
93	Can add investment	24	add_investment
94	Can change investment	24	change_investment
95	Can delete investment	24	delete_investment
96	Can view investment	24	view_investment
\.


--
-- Data for Name: business_contents; Type: TABLE DATA; Schema: public; Owner: gli
--

COPY public.business_contents (created_at, updated_at, id, section, title, subtitle, content, image_url, "order", status, meta_data) FROM stdin;
\.


--
-- Data for Name: development_timelines; Type: TABLE DATA; Schema: public; Owner: gli
--

COPY public.development_timelines (id, quarter, status_icon, title_ko, title_en, description_ko, description_en, "order", is_active, created_at, updated_at) FROM stdin;
75e9555a-d885-43b1-8def-7cfac41509de	2025 Q2	🟩	IR 및 법인 설립 준비	IR & Entity Setup	IR 자료 및 홍보 콘텐츠 제작을 완료하고, 법인 설립 및 해외 ESTA 관련 초기 행정 절차를 진행합니다.	Complete IR and marketing materials, and initiate corporate setup and overseas administrative (ESTA) procedures.	1	t	2025-10-21 01:13:17.181935+09	2025-10-21 01:13:17.181947+09
29c6767b-63a9-4fac-9b3c-f9997694186e	2025 Q3	🟩	글로벌 여행 및 레저 상품 기획	Global Travel & Leisure Product Planning	해외 파트너사와 협력하여 여행·레저 상품을 공동 기획하고 현지 제휴 체계를 마련합니다.	Collaborate with global partners to co-develop travel and leisure products and establish local alliances.	2	t	2025-10-21 01:13:17.186403+09	2025-10-21 01:13:17.186415+09
21190fda-ad83-455f-a3ed-33623b73d7e7	2025 Q4	⏳	웹 플랫폼 개발 착수	Web Platform Development Start	GLI 생태계의 핵심인 웹 플랫폼 개발을 시작하고, UX·UI 및 백엔드 구조 설계를 완료합니다.	Begin core web platform development for the GLI ecosystem, completing UX/UI and backend architecture design.	3	t	2025-10-21 01:13:17.190647+09	2025-10-21 01:13:17.190658+09
7342d07f-3350-47e6-8280-3ee24ccebb35	2026 Q1	🕐	해외 실물자산(RWA) 프로젝트 개발	Overseas RWA Project Development	해외 리조트·호텔 등 실물자산 기반 프로젝트를 발굴하고, RWA 토큰 발행 구조를 설계합니다.	Identify overseas asset-backed projects such as resorts and hotels, and design the RWA token issuance model.	4	t	2025-10-21 01:13:17.19459+09	2025-10-21 01:13:17.194603+09
e6ef9b29-d42e-4dd7-8315-fc8b2de345f3	2026 Q2	⏳	GLI 플랫폼 핵심 토큰 발행	GLI Core Token Issuance	GLIB / GLID / GLIL 토큰을 발행하고, 온체인 기반의 지갑 연동 시스템을 구축합니다.	Issue GLIB / GLID / GLIL tokens and deploy on-chain wallet integration systems.	5	t	2025-10-21 01:13:17.198419+09	2025-10-21 01:13:17.19843+09
55da4e7a-48b5-48bb-ac2b-d2fdb9cde55f	2026 Q3	🟩	멤버십 여행 플랫폼 출시	Launch of Membership Travel Platform	멤버십 기반 여행 및 레저 상품을 정식 출시하며, 글로벌 이용자를 대상으로 커뮤니티를 확장합니다.	Launch the membership-based travel and leisure platform, expanding community engagement worldwide.	6	t	2025-10-21 01:13:17.202837+09	2025-10-21 01:13:17.202852+09
8595afb3-de1b-49e3-9ff3-a72bb7d62741	2026 Q4	🕐	SERIES A 펀딩	Series A Funding	60억 원 규모의 시드 펀딩에 이어, 플랫폼 고도화 및 글로벌 확장을 위한 Series A 라운드를 진행합니다.	Following the 6B KRW seed funding, initiate Series A round for platform expansion and global scaling.	7	t	2025-10-21 01:13:17.206737+09	2025-10-21 01:13:17.206761+09
d8d10fc1-5d6a-4c04-a09d-6c55d6e7c6ae	2027 Q2	⏳	디지털자산 거래소 개발	Digital Asset Exchange Development	STO 및 가상자산이 통합된 라이선스 기반 거래소를 구축하고, DeFi 생태계 확장을 위한 연동 시스템을 개발합니다.	Develop a licensed exchange integrating STO and crypto markets, with DeFi ecosystem interoperability.	8	t	2025-10-21 01:13:17.212227+09	2025-10-21 01:13:17.212238+09
172d77df-4807-4eb5-9813-f61bddb72707	2028 Q1	🟩	거래소 정식 오픈	Exchange Official Launch	디지털자산 거래소를 정식 오픈하여, GLI 생태계 내 자산 순환 구조를 완성합니다.	Officially launch the digital asset exchange, completing GLI's internal asset circulation ecosystem.	9	t	2025-10-21 01:13:17.216414+09	2025-10-21 01:13:17.216425+09
70fc6037-ea51-498f-bde4-c8199fdc4085	2029 Q2	🚀	IPO (나스닥 상장 추진)	IPO (NASDAQ Listing Initiative)	글로벌 소셜 게이밍 및 투자 생태계를 기반으로 북미 중심의 IPO를 추진합니다.	Pursue IPO on NASDAQ, leveraging global social gaming and investment ecosystem.	10	t	2025-10-21 01:13:17.220269+09	2025-10-21 01:13:17.220281+09
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: gli
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: gli
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	auth	permission
2	auth	group
3	contenttypes	contenttype
4	solana_auth	authnonce
5	solana_auth	solanauser
6	solana_auth	solanatransaction
7	solana_auth	faceverification
8	solana_auth	admingrade
9	solana_auth	adminpermission
10	solana_auth	adminuser
11	solana_auth	gradepermission
12	solana_auth	teammember
13	solana_auth	projectfeature
14	solana_auth	strategyphase
15	solana_auth	developmenttimeline
16	solana_auth	tokenecosystem
17	gli_content	rwacategory
18	gli_content	shoppingcategory
19	gli_content	businesscontent
20	gli_content	rwaasset
21	gli_content	shoppingorder
22	gli_content	shoppingproduct
23	gli_content	shoppingorderitem
24	gli_content	investment
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: gli
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2025-10-20 22:39:24.854515+09
2	contenttypes	0002_remove_content_type_name	2025-10-20 22:39:35.817981+09
3	auth	0001_initial	2025-10-20 22:39:35.826051+09
4	auth	0002_alter_permission_name_max_length	2025-10-20 22:39:35.827975+09
5	auth	0003_alter_user_email_max_length	2025-10-20 22:39:35.829745+09
6	auth	0004_alter_user_username_opts	2025-10-20 22:39:35.831329+09
7	auth	0005_alter_user_last_login_null	2025-10-20 22:39:35.832786+09
8	auth	0006_require_contenttypes_0002	2025-10-20 22:39:35.834272+09
9	auth	0007_alter_validators_add_error_messages	2025-10-20 22:39:35.835896+09
10	auth	0008_alter_user_username_max_length	2025-10-20 22:39:35.837936+09
11	auth	0009_alter_user_last_name_max_length	2025-10-20 22:39:35.839842+09
12	auth	0010_alter_group_name_max_length	2025-10-20 22:39:35.841694+09
13	auth	0011_update_proxy_permissions	2025-10-20 22:39:35.843945+09
14	auth	0012_alter_user_first_name_max_length	2025-10-20 22:39:35.845975+09
15	solana_auth	0001_initial	2025-10-20 22:39:35.849169+09
16	solana_auth	0002_make_wallet_address_optional	2025-10-20 22:39:35.851361+09
17	solana_auth	0003_faceverification	2025-10-20 22:39:35.853521+09
18	solana_auth	0004_admingrade_adminpermission_adminuser_gradepermission	2025-10-20 22:39:35.85554+09
19	solana_auth	0005_teammember	2025-10-20 22:39:35.857141+09
20	solana_auth	0006_projectfeature	2025-10-20 22:39:35.85913+09
21	solana_auth	0007_strategyphase	2025-10-20 22:39:35.860937+09
22	solana_auth	0008_developmenttimeline_tokenecosystem	2025-10-20 22:39:35.862826+09
23	solana_auth	0009_solanauser_vpx_experience_solanauser_vpx_partner_and_more	2025-10-20 22:39:35.864569+09
24	solana_auth	0010_make_image_url_optional	2025-10-20 22:39:35.866607+09
25	solana_auth	0011_add_name_fields_to_team_member	2025-10-20 22:39:35.868331+09
26	solana_auth	0012_split_strategy_phase_features_to_ko_en	2025-10-20 22:40:43.516883+09
27	solana_auth	0013_remove_tokenecosystem_features_and_more	2025-10-21 01:23:27.554774+09
28	gli_content	0001_initial	2025-10-21 01:59:05.656335+09
29	gli_content	0002_rwaasset_area_sqm_rwaasset_asset_location_en_and_more	2025-10-21 01:59:12.273126+09
32	gli_content	0003_rename_gleb_to_glib	2025-10-21 13:49:41.991215+09
33	gli_content	0004_shoppingcategory_description_en_and_more	2025-10-21 14:05:45.348212+09
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: gli
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
\.


--
-- Data for Name: face_verifications; Type: TABLE DATA; Schema: public; Owner: gli
--

COPY public.face_verifications (id, verified, confidence, liveness_score, attempts, check_details, verification_timestamp, created_at, updated_at, user_id) FROM stdin;
\.


--
-- Data for Name: grade_permissions; Type: TABLE DATA; Schema: public; Owner: gli
--

COPY public.grade_permissions (id, created_at, grade_id, permission_id) FROM stdin;
\.


--
-- Data for Name: investments; Type: TABLE DATA; Schema: public; Owner: gli
--

COPY public.investments (created_at, updated_at, id, amount_glib, amount_usd_at_time, investment_date, expected_return_date, lock_end_date, expected_apy_at_time, current_value_glib, realized_profit_glib, status, investment_tx_hash, withdrawal_tx_hash, metadata, investor_id, rwa_asset_id) FROM stdin;
\.


--
-- Data for Name: project_features; Type: TABLE DATA; Schema: public; Owner: gli
--

COPY public.project_features (id, icon, title_ko, title_en, description_ko, description_en, "order", is_active, created_at, updated_at) FROM stdin;
8015fb5c-fa9b-46eb-bc90-89a9bdf0288e	💸	I - INVESTMENT : 왜 실물자산(RWA) 기반 블록체인인가?	I - INVESTMENT : Why a Real Asset-Based Blockchain (RWA)?	온체인 실물자산은 스테이킹이나 파밍 등 다양한 DeFi 상품으로 활용이 가능하여, 단순 임대나 대여 수익에 그쳤던 오프라인 실물자산과 달리 새로운 가치를 창출할 수 있습니다. 또한 화폐 기반 스테이블코인은 중앙집중적 구조로 인플레이션에 취약하지만, 온체인 실물자산 토큰은 탈중앙화가 가능하고 인플레이션에 강한 안정적 자산입니다. 더불어 DeFi의 고수익률이 일시적이고 변동성이 큰 반면, 부동산 등의 실물자산은 임대 수익을 기반으로 지속 가능한 수익을 제공하며, 이를 블록체인과 결합하면 안정적인 수익 창출이 가능합니다.	On-chain real-world assets can be utilized in various DeFi products such as staking and farming, creating new value beyond the simple rental or leasing income of traditional offline assets. While fiat-based stablecoins are centralized and vulnerable to inflation, on-chain asset tokens are decentralized and serve as stable, inflation-resistant assets. Moreover, unlike the temporary and volatile high yields of DeFi, real-world assets like real estate generate sustainable rental income, and when combined with blockchain, they enable stable and continuous profit generation.	3	t	2025-10-20 10:39:55.331+09	2025-10-20 10:47:21.768+09
cd584d4a-545e-4ed8-a808-99d233155954	🎰	G - GAME : 소셜 카지노	G - GAME : Social CASINO	네오위즈는 마카오의 LT게임과 슬롯 소프트웨어 공급 계약을 통해 B2B 시장을 확대하고, 개발비와 고정비가 낮은 소셜 카지노 사업 특성으로 30~40%의 높은 영업이익률을 유지하고 있습니다. 또한 강원랜드와의 슬롯머신 공동개발 협약으로 온·오프라인 카지노 산업을 연계하며 안정적인 고수익 구조를 구축했습니다.	Neowiz has expanded its B2B presence by supplying slot software to Macau’s LT Game, maintaining a high operating margin of 30–40% due to the low-cost nature of its social casino business. Through an exclusive slot machine co-development agreement with Kangwon Land, the company has integrated online and offline casino operations, establishing a stable and highly profitable structure.	1	t	2025-10-20 10:35:19.976+09	2025-10-20 10:53:31.609+09
f848d283-b3aa-4f1b-9fd8-e838fa193d30	🏨	L – LEISURE : 새로운 형태의 디지털 레저 산업	L – LEISURE: A New Form of Digital Recreation Industry	온체인 레저 산업은 단순한 여가 활동을 넘어 참여와 보상, 그리고 자산화가 결합된 새로운 시장을 형성하고 있습니다. 이용자는 게임, 스포츠, 여행 등 다양한 레저 활동을 통해 토큰이나 NFT를 획득하고, 이를 거래하거나 보유함으로써 실질적인 경제적 가치를 얻을 수 있습니다. 이러한 구조는 기존의 소비 중심 레저 시장을 참여형·수익형 생태계로 전환시키며, 오프라인과 온라인을 아우르는 디지털 자산 기반 레저 경제를 만들어가고 있습니다.	The on-chain leisure industry is evolving beyond traditional recreation, forming a new market that combines participation, rewards, and assetization. Users can earn tokens or NFTs through activities such as gaming, sports, or travel, gaining tangible economic value by trading or holding them. This model transforms the consumption-driven leisure market into a participatory and profit-generating ecosystem, bridging offline and online experiences to establish a digital asset–based leisure economy.	2	t	2025-10-20 10:53:00.143+09	2025-10-20 10:55:03.897+09
\.


--
-- Data for Name: rwa_assets; Type: TABLE DATA; Schema: public; Owner: gli
--

COPY public.rwa_assets (created_at, updated_at, id, name, description, short_description, total_value_usd, min_investment_glib, max_investment_glib, expected_apy, historical_returns, risk_level, risk_factors, investment_period_months, lock_period_months, asset_location, asset_type, underlying_assets, main_image_url, image_urls, document_urls, total_invested_glib, investor_count, funding_target_glib, status, is_featured, metadata, category_id, area_sqm, asset_location_en, asset_type_en, description_en, name_en, operation_type, short_description_en) FROM stdin;
2025-10-21 03:08:34.54959+09	2025-10-21 04:29:32.650111+09	a619424a-b8c5-4d37-b4de-d28aaaeb26ee	호치민 ERA 부동산	호치민 7군 푸미흥 비즈니스 지구 오피스 투자\n\n주요 특징:\n- 신흥 비즈니스 지구 중심 입지\n- 외국계 기업 임차인 다수\n- 안정적인 임대 수익 구조\n\n투자 포인트:\n1. 호치민 경제 성장 수혜\n2. 외국계 기업 수요 증가\n3. 안정적인 상업용 부동산\n4. 장기 임대 계약 기반	호치민 신흥 비즈니스 지구의 오피스 빌딩 투자 프로젝트입니다.	6000000.00	150.00000000	60000000.00000000	9.50	[]	medium	[]	36	12	호치민 7군 푸미흥 비즈니스 지구	상업용	{}	https://gli-platform-media-staging.s3.ap-northeast-2.amazonaws.com/business-content/1e4c0657c8414b5489e072261c1c3dd4_20251021_042931.png	[]	[]	0.00000000	0	\N	active	f	{}	d63d79db-6cff-420f-a63a-0680ad8c7bcc	4500.00	Phu My Hung Business District, District 7, Ho Chi Minh	Commercial	Office investment in Phu My Hung District 7, HCMC\n\nKey Features:\n- Prime location in emerging business district\n- Multiple foreign corporate tenants\n- Stable rental income structure\n\nInvestment Highlights:\n1. Benefits from HCMC economic growth\n2. Increasing foreign corporate demand\n3. Stable commercial real estate\n4. Long-term lease agreements	ERA Real Estate, Ho Chi Minh City	rental	Office property investment in the emerging Phu My Hung business district.
2025-10-21 03:08:34.600617+09	2025-10-21 04:47:10.690987+09	0185f402-ac21-4304-9373-948c79496bb7	세부 RYOUKU 고급 일식 리조트	일본식 프리미엄 레저 리조트\n\n주요 특징:\n- 일본 브랜드 제휴 운영\n- 막탄섬 해안 프라임 입지\n- 일본식 온천 및 스파 시설\n\n투자 포인트:\n1. 일본 관광객 타깃\n2. 프리미엄 브랜드 파워\n3. 차별화된 일본식 서비스\n4. 막탄섬 관광 허브 입지	일본 프랜차이즈와 제휴한 세부 고급 레저 리조트 프로젝트입니다.	9000000.00	300.00000000	90000000.00000000	12.50	[]	medium	[]	36	12	필리핀 세부 막탄섬 해안	리조트	{}	https://gli-platform-media-staging.s3.ap-northeast-2.amazonaws.com/business-content/07833508316f4f66b239553d9c8f9ed7_20251021_044709.png	[]	[]	0.00000000	0	\N	active	f	{}	d63d79db-6cff-420f-a63a-0680ad8c7bcc	12000.00	Mactan Island Coast, Cebu, Philippines	Resort	Japanese-style premium leisure resort\n\nKey Features:\n- Japanese brand partnership\n- Prime Mactan Island beachfront location\n- Japanese-style onsen and spa facilities\n\nInvestment Highlights:\n1. Targeting Japanese tourists\n2. Premium brand power\n3. Differentiated Japanese-style service\n4. Mactan Island tourism hub location	RYOUKU Japanese Resort, Cebu	consignment	A premium Japanese-branded resort project located on Cebu's Mactan Island.
2025-10-21 03:08:34.590521+09	2025-10-21 04:47:18.65037+09	72c06b30-f54e-46c3-90fb-61e58627d7e8	말레이시아 두리안 농장 RWA 프로젝트	말레이시아 프리미엄 두리안 농장 투자\n\n주요 특징:\n- 고급 무산왕(Musang King) 품종\n- 중국 수출 중심 판로\n- 수확 기반 수익 분배\n\n투자 포인트:\n1. 중국 두리안 수요 급증\n2. 프리미엄 품종 생산\n3. 높은 수익률 가능성\n4. 농업 자산 다변화\n\n리스크:\n- 기후 및 작황 변동성\n- 수출 규제 변화 가능성	고급 두리안 수출용 농장에 대한 수익 분배형 투자입니다.	2800000.00	80.00000000	28000000.00000000	15.00	[]	high	[]	36	12	말레이시아 파항주	생산형	{}	https://gli-platform-media-staging.s3.ap-northeast-2.amazonaws.com/business-content/a07a94aaa83d478ca018878df120c1de_20251021_044717.png	[]	[]	0.00000000	0	\N	active	f	{}	d63d79db-6cff-420f-a63a-0680ad8c7bcc	25000.00	Pahang, Malaysia	Production	Premium durian farm investment in Malaysia\n\nKey Features:\n- Premium Musang King variety\n- China export-focused distribution\n- Harvest-based revenue sharing\n\nInvestment Highlights:\n1. Surging durian demand in China\n2. Premium variety production\n3. High yield potential\n4. Agricultural asset diversification\n\nRisks:\n- Climate and crop volatility\n- Potential export regulation changes	Durian Farm RWA Project, Malaysia	consignment	Revenue-sharing investment in export-grade durian farm.
2025-10-21 03:08:34.610932+09	2025-10-21 04:49:02.199466+09	6237b6c1-f236-4ecd-a130-557efb4072d5	Xijiu 싱가포르 브랜드 콘텐츠 투자	Xijiu 글로벌 브랜드 콘텐츠 사업\n\n주요 특징:\n- 중국 명주 브랜드 글로벌 확장\n- 싱가포르 허브 라이프스타일 콘텐츠\n- 브랜드 마케팅 수익 배당\n\n투자 포인트:\n1. 중국 명품 주류 브랜드\n2. 동남아 시장 진출 전략\n3. 콘텐츠 및 브랜딩 수익\n4. 라이프스타일 비즈니스 확장	중국 명주 Xijiu 브랜드의 글로벌 라이프스타일 콘텐츠 사업 투자.	5500000.00	150.00000000	55000000.00000000	10.00	[]	medium	[]	36	12	싱가포르 Marina Bay	콘텐츠	{}	https://gli-platform-media-staging.s3.ap-northeast-2.amazonaws.com/business-content/ecf3d06c9c8f4e4ca9e46548de7b10db_20251021_044900.png	[]	[]	0.00000000	0	\N	active	f	{}	d63d79db-6cff-420f-a63a-0680ad8c7bcc	800.00	Marina Bay, Singapore	Content	Xijiu global brand content business\n\nKey Features:\n- Global expansion of Chinese premium liquor brand\n- Singapore-based lifestyle content hub\n- Brand marketing revenue distribution\n\nInvestment Highlights:\n1. Chinese luxury liquor brand\n2. Southeast Asia market entry strategy\n3. Content and branding revenue\n4. Lifestyle business expansion	Xijiu Brand Content Investment, Singapore	other	Investment in global lifestyle brand expansion of China's Xijiu liquor company.
2025-10-21 03:08:34.560056+09	2025-10-21 04:29:02.24475+09	cb7b6027-dd4e-4eb4-8f3f-158077d8ec84	마닐라 Vista Land 부동산	마닐라 BGC 인근 중고급 주거용 부동산\n\n주요 특징:\n- 안정적인 임대 수익 구조\n- 중산층 및 외국인 거주자 타깃\n- 낮은 위험도의 안정형 자산\n\n투자 포인트:\n1. BGC 비즈니스 지구 인접\n2. 안정적인 주거 수요\n3. 낮은 공실률\n4. 보수적 투자자에 적합	안정적인 임대 수익을 창출하는 중고급 주거 프로젝트입니다.	4000000.00	100.00000000	40000000.00000000	8.70	[]	low	[]	36	12	필리핀 마닐라 Bonifacio Global City 인근	주거용	{}	https://gli-platform-media-staging.s3.ap-northeast-2.amazonaws.com/business-content/662f48187c474538b0cc1a58bb304673_20251021_042900.png	[]	[]	0.00000000	0	\N	active	f	{}	d63d79db-6cff-420f-a63a-0680ad8c7bcc	3200.00	Near Bonifacio Global City, Manila, Philippines	Residential	Mid-to-high-end residential property near BGC Manila\n\nKey Features:\n- Stable rental income structure\n- Targeting middle class and expat residents\n- Low-risk stable asset\n\nInvestment Highlights:\n1. Adjacent to BGC business district\n2. Stable residential demand\n3. Low vacancy rate\n4. Suitable for conservative investors	Vista Land Property, Manila	rental	Mid-to-high-end residential project generating steady rental yields.
2025-10-21 03:08:34.569411+09	2025-10-21 04:37:48.695478+09	39f8ad8f-4838-490d-b87e-4f384c7d5898	세부 Waterfront Hotel & Casino	세부 대표 복합 카지노 리조트\n\n주요 특징:\n- 호텔, 카지노, 레스토랑 복합 운영\n- 관광객 유입 급증 지역\n- 연평균 13% 이상 수익률 예상\n\n투자 포인트:\n1. 필리핀 제2의 도시 세부 입지\n2. 복합 엔터테인먼트 시설\n3. 높은 수익률 잠재력\n4. 관광산업 성장 수혜	세부 최대 복합 카지노 리조트 중 하나로, 관광객 유입이 급증하고 있습니다.	12000000.00	500.00000000	120000000.00000000	13.20	[]	medium	[]	36	12	필리핀 세부 IT Park 인근	호텔형	{}	https://gli-platform-media-staging.s3.ap-northeast-2.amazonaws.com/business-content/9261985450a046c792b2b9a8f1c2c90b_20251021_043747.png	[]	[]	0.00000000	0	\N	active	f	{}	d63d79db-6cff-420f-a63a-0680ad8c7bcc	18000.00	Near IT Park, Cebu, Philippines	Hotel	Leading integrated casino resort in Cebu\n\nKey Features:\n- Hotel, casino, restaurant complex\n- Growing tourist destination\n- Expected annual yield above 13%\n\nInvestment Highlights:\n1. Located in Cebu, Philippines' 2nd largest city\n2. Integrated entertainment facility\n3. High yield potential\n4. Tourism industry growth benefits	Waterfront Hotel & Casino, Cebu	consignment	One of Cebu's largest integrated casino resorts with growing tourist influx.
2025-10-21 03:08:34.533168+09	2025-10-21 04:29:18.155886+09	cecbaf2e-bedf-41ec-9bd6-aa5037f3e0f2	호이안 리조트 & 골프	베트남 중부 호이안 해변 인근 프리미엄 리조트\n\n주요 특징:\n- 18홀 챔피언십 골프 코스\n- 외국인 관광객 비중 70% 이상\n- 안정적 숙박·그린피 수익\n\n투자 포인트:\n1. 유네스코 세계문화유산 도시 인근\n2. 골프 관광 복합 시설\n3. 높은 외국인 관광객 비중\n4. 다변화된 수익 구조	베트남 중부의 명소 호이안에 위치한 프리미엄 리조트 & 골프 클럽입니다.	10000000.00	300.00000000	100000000.00000000	10.80	[]	medium	[]	36	12	베트남 꽝남성 호이안 해변 인근	리조트	{}	https://gli-platform-media-staging.s3.ap-northeast-2.amazonaws.com/business-content/62b18e882e89467683feff2051c23a65_20251021_042916.png	[]	[]	0.00000000	0	\N	active	f	{}	d63d79db-6cff-420f-a63a-0680ad8c7bcc	15000.00	Near Hoi An Beach, Quang Nam, Vietnam	Resort	Premium resort near Hoi An Beach, Central Vietnam\n\nKey Features:\n- 18-hole championship golf course\n- 70% foreign visitor ratio\n- Stable income from lodging and golf fees\n\nInvestment Highlights:\n1. Near UNESCO World Heritage city\n2. Golf tourism complex facility\n3. High proportion of international tourists\n4. Diversified revenue streams	Hoi An Resort & Golf	consignment	A premium resort and golf club located in the central Vietnamese city of Hoi An.
2025-10-21 03:08:34.521018+09	2025-10-21 04:30:12.090659+09	13cbe358-17f5-43b1-a560-d2d474072000	캄보디아 시아누크빌 Star Bay 리조트	시아누크빌 중심 해안도로에 위치\n\n주요 특징:\n- 평균 객실 점유율 82%\n- 현지 정부 관광 인센티브 대상\n- 연평균 수익률 10~12% 예상\n\n투자 포인트:\n1. 캄보디아 신흥 휴양 도시의 성장 잠재력\n2. 중국 및 아시아 관광객 증가 추세\n3. 정부 관광 인센티브 혜택\n4. 안정적인 해안 리조트 운영	캄보디아의 신흥 휴양지에 위치한 해안 리조트로, 안정적인 관광 수익 창출이 가능합니다.	8000000.00	200.00000000	80000000.00000000	11.20	[]	medium	[]	36	12	캄보디아 시아누크빌 해안도로 인근	리조트	{}	https://gli-platform-media-staging.s3.ap-northeast-2.amazonaws.com/business-content/93744357c3794e869ac310e8f4d5d5fd_20251021_043010.png	[]	[]	0.00000000	0	\N	active	f	{}	d63d79db-6cff-420f-a63a-0680ad8c7bcc	8500.00	Near coastal road, Sihanoukville, Cambodia	Resort	Located along Sihanoukville's main coastal road\n\nKey Features:\n- 82% average occupancy rate\n- Eligible for local government tourism incentives\n- Expected annual yield: 10–12%\n\nInvestment Highlights:\n1. Growth potential in Cambodia's emerging resort city\n2. Increasing Chinese and Asian tourist arrivals\n3. Government tourism incentive benefits\n4. Stable beachfront resort operations	Star Bay Resort, Sihanoukville, Cambodia	consignment	A beachfront resort in Cambodia's emerging coastal city, generating stable tourism revenue.
2025-10-21 03:08:34.579239+09	2025-10-21 04:40:57.846399+09	969bfea8-284f-4cfb-95b0-a85807cbc5a3	Brown Coffee 프랜차이즈	캄보디아 1위 커피 브랜드 프랜차이즈\n\n주요 특징:\n- 현지 시장 점유율 1위\n- 신규 매장 투자형 모델\n- 안정적인 프랜차이즈 수익\n\n투자 포인트:\n1. 캄보디아 커피 시장 성장\n2. 검증된 브랜드 파워\n3. 프랜차이즈 수익 분배 모델\n4. 비교적 낮은 투자금	캄보디아 대표 커피 브랜드 Brown의 신규 매장 투자형 프랜차이즈입니다.	3500000.00	100.00000000	35000000.00000000	14.00	[]	medium	[]	36	12	프놈펜, 캄보디아	프랜차이즈	{}	https://gli-platform-media-staging.s3.ap-northeast-2.amazonaws.com/business-content/593d580d14ea401c9b0a4672fba87596_20251021_044057.png	[]	[]	0.00000000	0	\N	active	f	{}	d63d79db-6cff-420f-a63a-0680ad8c7bcc	150.00	Phnom Penh, Cambodia	Franchise	Cambodia's #1 coffee brand franchise\n\nKey Features:\n- Market leader in Cambodia\n- New store investment model\n- Stable franchise revenue\n\nInvestment Highlights:\n1. Growing coffee market in Cambodia\n2. Proven brand power\n3. Franchise revenue sharing model\n4. Relatively low investment amount	Brown Coffee Franchise Cambodia	direct	Investment franchise for Brown, Cambodia's leading coffee brand.
2025-10-21 03:08:34.621259+09	2025-10-21 04:51:44.297799+09	7a07998e-ff46-4c59-87b9-7fc6edca91a1	마카오 Sands Group 카지노 지분 참여	마카오 대표 카지노 그룹 지분 투자\n\n주요 특징:\n- Sands Group 지분 참여형\n- 코타이 스트립 프라임 입지\n- 고수익 고위험 구조\n\n투자 포인트:\n1. 세계 최대 카지노 시장 마카오\n2. 업계 1위 그룹 지분 투자\n3. 높은 수익률 가능성\n4. 중국 관광객 회복 수혜\n\n리스크:\n- 규제 변화 리스크\n- 경기 민감도 높음\n- 최소 투자금 상대적 고액	마카오 최대 카지노 그룹의 지분형 RWA 프로젝트입니다.	20000000.00	1000.00000000	200000000.00000000	16.30	[]	high	[]	36	12	마카오 Cotai Strip	지분형	{}	https://gli-platform-media-staging.s3.ap-northeast-2.amazonaws.com/business-content/b6ef2a04b30f4826975d16ca3bacb543_20251021_045143.png	[]	[]	0.00000000	0	\N	active	f	{}	d63d79db-6cff-420f-a63a-0680ad8c7bcc	50000.00	Cotai Strip, Macau	Equity	Equity investment in Macau's leading casino group\n\nKey Features:\n- Sands Group equity participation\n- Prime Cotai Strip location\n- High-risk high-return structure\n\nInvestment Highlights:\n1. Macau, world's largest casino market\n2. Industry leader equity investment\n3. High yield potential\n4. Chinese tourist recovery benefits\n\nRisks:\n- Regulatory change risks\n- High economic sensitivity\n- Relatively high minimum investment	Sands Group Casino Equity, Macau	other	Equity-based RWA project in Macau's leading casino group.
2025-10-21 02:01:13.631711+09	2025-10-21 05:00:02.010594+09	1a6918d2-e965-413d-a3ce-eb7e90a6ec91	제주도 프리미엄 리조트	제주도 서귀포시에 위치한 프리미엄 리조트입니다.\n\n주요 특징:\n- 오션뷰가 보이는 50개의 객실\n- 연중 높은 객실 점유율 (평균 85%)\n- 안정적인 임대 수익 구조\n- 연 8-12% 수익률 예상\n\n투자 포인트:\n1. 제주도 관광객 증가 추세\n2. 프리미엄 숙박 시설 수요 증가\n3. 전문 운영사의 위탁 운영\n4. 분기별 배당 지급\n\n리스크:\n- 계절적 수요 변동\n- 관광객 수 변화에 따른 수익률 변동\n- 시설 유지보수 비용\n\n본 자산은 GLI-B 토큰으로 투자 가능하며, 최소 투자금액은 100 GLEB입니다.	제주도 서귀포 오션뷰 프리미엄 리조트, 연 8-12% 수익률	5000000.00	100.00000000	50000000.00000000	10.50	[{"year": 2023, "return": 11.2}, {"year": 2022, "return": 9.8}, {"year": 2021, "return": 10.5}]	medium	["계절적 수요 변동", "관광객 수 변화", "환율 변동", "시설 노후화"]	36	12	제주특별자치도 서귀포시 중문관광로 72번길	real-estate	{"facilities": [{"type": "객실", "count": 50, "avg_size_sqm": 45}, {"type": "레스토랑", "count": 2, "size_sqm": 300}, {"type": "수영장", "count": 1, "size_sqm": 500}, {"type": "스파", "count": 1, "size_sqm": 200}], "land_value": 2000000, "building_value": 3000000}	https://gli-platform-media-staging.s3.ap-northeast-2.amazonaws.com/business-content/decc66614f4b4e3c8d9795a9d549b22f_20251021_050000.png	["https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=800", "https://images.unsplash.com/photo-1582719508461-905c673771fd?w=800", "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800", "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800"]	[{"url": "/documents/resort-prospectus.pdf", "name": "투자설명서.pdf"}, {"url": "/documents/resort-appraisal.pdf", "name": "감정평가서.pdf"}, {"url": "/documents/resort-operation-plan.pdf", "name": "운영계획서.pdf"}]	3500.00000000	12	50000.00000000	active	f	{"operator": "제주리조트운영(주)", "amenities": ["와이파이", "주차장", "조식 포함", "픽업 서비스", "해변 접근"], "languages": ["한국어", "영어", "중국어", "일본어"], "certifications": ["친환경 건축물 인증", "관광숙박업 등록"], "completion_date": "2020-06-15", "last_renovation": "2023-01-10"}	d63d79db-6cff-420f-a63a-0680ad8c7bcc	12500.50	72-gil, Jungmun Tourism-ro, Seogwipo-si, Jeju-do, South Korea	Resort	as fsdfasdf	asfasdfasdfas dfs	consignment	fasdf asdf
\.


--
-- Data for Name: rwa_categories; Type: TABLE DATA; Schema: public; Owner: gli
--

COPY public.rwa_categories (created_at, updated_at, id, name, description, icon, "order", is_active) FROM stdin;
2025-10-21 02:01:13.61513+09	2025-10-21 02:01:13.615149+09	d63d79db-6cff-420f-a63a-0680ad8c7bcc	부동산	실물 부동산 투자	🏢	1	t
2025-10-21 03:08:34.471037+09	2025-10-21 03:08:34.471059+09	d6699ecd-a9e7-4c1b-8e21-6b2f6f35a204	카지노	카지노 및 복합 리조트	🎰	2	t
2025-10-21 03:08:34.479498+09	2025-10-21 03:08:34.479553+09	28ee1da1-a1d3-47b4-accd-2e866ff668f5	사업 아이템	프랜차이즈 및 사업 투자	💼	3	t
2025-10-21 03:08:34.487304+09	2025-10-21 03:08:34.48732+09	678cde9d-07d1-4c53-97b4-67d24548c1e9	농업	농업 및 생산형 자산	🌾	4	t
2025-10-21 03:08:34.495857+09	2025-10-21 03:08:34.49592+09	c587897d-ed66-4745-b6ba-60be2940c004	레저	레저 및 휴양 시설	⛱️	5	t
2025-10-21 03:08:34.503911+09	2025-10-21 03:08:34.503932+09	11f03750-5b6d-4238-96a3-fc51923aaf53	브랜드	브랜드 및 콘텐츠 사업	🏷️	6	t
\.


--
-- Data for Name: shopping_categories; Type: TABLE DATA; Schema: public; Owner: gli
--

COPY public.shopping_categories (created_at, updated_at, id, name, description, icon, "order", is_active, description_en, name_en) FROM stdin;
2025-10-21 04:51:38.07187+09	2025-10-21 04:51:38.072401+09	d624364e-e997-430d-91ef-3ef0171a11fc	리조트&호텔 예약	GLI-L 토큰으로 예약할 수 있는 프리미엄 리조트와 호텔	🏨	1	t		
2025-10-21 04:51:38.083436+09	2025-10-21 04:51:38.083455+09	04617999-d1c9-4a59-b688-546211820c45	상품	GLI-L 토큰으로 구매할 수 있는 프리미엄 상품들	🛍️	2	t		
2025-10-21 04:51:38.089255+09	2025-10-21 04:51:38.089268+09	7440548d-5680-4b9f-b930-42aad4a8a638	레스토랑	GLI-L 토큰으로 예약할 수 있는 파인 다이닝 레스토랑	🍽️	3	t		
\.


--
-- Data for Name: shopping_order_items; Type: TABLE DATA; Schema: public; Owner: gli
--

COPY public.shopping_order_items (created_at, updated_at, id, product_name, product_price_glil, quantity, selected_attributes, order_id, product_id) FROM stdin;
\.


--
-- Data for Name: shopping_orders; Type: TABLE DATA; Schema: public; Owner: gli
--

COPY public.shopping_orders (created_at, updated_at, id, order_number, total_amount_glil, total_amount_usd, status, payment_tx_hash, paid_at, shipping_address, tracking_number, shipped_at, delivered_at, notes, metadata, customer_id) FROM stdin;
\.


--
-- Data for Name: shopping_products; Type: TABLE DATA; Schema: public; Owner: gli
--

COPY public.shopping_products (created_at, updated_at, id, name, description, short_description, product_type, price_glil, price_usd, stock_quantity, unlimited_stock, main_image_url, image_urls, status, is_featured, tags, attributes, view_count, purchase_count, category_id, description_en, name_en, short_description_en) FROM stdin;
2025-10-21 04:51:38.161397+09	2025-10-21 04:51:38.16142+09	01a22a61-eea0-499a-84c8-e8d241425b20	GLI 요가매트	프리미엄 친환경 소재 요가매트입니다. 미끄럼 방지 기능과 쿠션감이 뛰어나 편안한 운동을 즐길 수 있습니다.	친환경 프리미엄 요가매트	goods	75.00000000	75.00	6	t	https://placehold.co/600x400/9370DB/FFFFFF/png?text=GLI+Yoga+Mat	[]	active	f	["스포츠", "요가", "매트", "운동", "Sports", "Yoga", "Mat", "Exercise"]	{"size": "183cm x 61cm", "colors": ["Purple", "Pink", "Blue", "Green"], "material": "TPE (Eco-Friendly)", "thickness": "6mm", "categoryId": "sports"}	0	0	04617999-d1c9-4a59-b688-546211820c45			
2025-10-21 04:51:38.103038+09	2025-10-21 04:51:38.103053+09	caf15173-4869-493f-91e7-3398a8b825f8	GLI Ocean Resort	제주도의 아름다운 해변가에 위치한 럭셔리 리조트입니다. 전 객실에서 오션뷰를 즐길 수 있으며, 최고급 편의시설을 갖추고 있습니다.	제주도 오션뷰 럭셔리 리조트	resort	150.00000000	150.00	50	t	https://placehold.co/800x600/1E90FF/FFFFFF/png?text=GLI+Ocean+Resort	[]	active	t	["오션뷰", "럭셔리", "제주도", "5성급", "Ocean View", "Luxury", "Jeju", "5-Star"]	{"rooms": [{"type": "standard", "price": 150, "type_ko": "스탠다드", "features": ["Ocean View", "Free WiFi", "Breakfast Included"], "features_ko": ["오션뷰", "무료 WiFi", "조식 포함"]}, {"type": "deluxe", "price": 250, "type_ko": "디럭스", "features": ["Premium Ocean View", "Balcony", "Room Service", "Mini Bar"], "features_ko": ["프리미엄 오션뷰", "발코니", "룸서비스", "미니바"]}, {"type": "suite", "price": 450, "type_ko": "스위트", "features": ["Panoramic View", "Separate Living Room", "Jacuzzi", "Butler Service"], "features_ko": ["파노라믹 뷰", "별도 거실", "자쿠지", "버틀러 서비스"]}], "rating": 5, "location": "Jeju Island, Korea", "location_en": "Jeju Island, Korea"}	0	0	d624364e-e997-430d-91ef-3ef0171a11fc			
2025-10-21 04:51:38.115892+09	2025-10-21 04:51:38.115907+09	1cf282f2-b443-4104-b753-459a5a5e1578	GLI Mountain Lodge	설악산의 청정 자연 속에서 힐링할 수 있는 마운틴 리조트입니다. 사계절 아름다운 경관과 함께 다양한 액티비티를 즐길 수 있습니다.	설악산 자연 속 힐링 리조트	resort	120.00000000	120.00	40	t	https://placehold.co/800x600/228B22/FFFFFF/png?text=GLI+Mountain+Lodge	[]	active	t	["산악", "자연", "설악산", "힐링", "Mountain", "Nature", "Seoraksan", "Healing"]	{"rooms": [{"type": "standard", "price": 120, "type_ko": "스탠다드", "features": ["Mountain View", "Heating", "Free Parking"], "features_ko": ["마운틴 뷰", "난방", "무료 주차"]}, {"type": "deluxe", "price": 200, "type_ko": "디럭스", "features": ["Premium Mountain View", "Fireplace", "Private Deck"], "features_ko": ["프리미엄 마운틴 뷰", "벽난로", "프라이빗 데크"]}, {"type": "villa", "price": 380, "type_ko": "빌라", "features": ["Private Villa", "Hot Tub", "Kitchen", "BBQ Area"], "features_ko": ["프라이빗 빌라", "온수 욕조", "주방", "BBQ 공간"]}], "rating": 4, "location": "Gangwon-do, Korea", "location_en": "Gangwon-do, Korea"}	0	0	d624364e-e997-430d-91ef-3ef0171a11fc			
2025-10-21 04:51:38.124041+09	2025-10-21 04:51:38.124056+09	b950e99b-44cf-4100-970d-4369b4865d4e	GLI City Hotel	서울 도심 속 비즈니스와 레저를 동시에 즐길 수 있는 프리미엄 호텔입니다. 최신 시설과 편리한 교통으로 완벽한 서울 여행을 경험하세요.	서울 도심 프리미엄 호텔	resort	180.00000000	180.00	60	t	https://placehold.co/800x600/FFD700/000000/png?text=GLI+City+Hotel	[]	active	t	["도심", "비즈니스", "서울", "편리", "City", "Business", "Seoul", "Convenient"]	{"rooms": [{"type": "standard", "price": 180, "type_ko": "스탠다드", "features": ["City View", "Business Center", "Gym Access"], "features_ko": ["시티 뷰", "비즈니스 센터", "헬스장 이용"]}, {"type": "deluxe", "price": 280, "type_ko": "디럭스", "features": ["Han River View", "Executive Lounge", "Express Check-in"], "features_ko": ["한강 뷰", "이그제큐티브 라운지", "빠른 체크인"]}, {"type": "suite", "price": 500, "type_ko": "스위트", "features": ["Presidential Suite", "Private Elevator", "Personal Assistant", "Rooftop Access"], "features_ko": ["프레지덴셜 스위트", "전용 엘리베이터", "개인 비서", "루프탑 이용"]}], "rating": 5, "location": "Seoul, Korea", "location_en": "Seoul, Korea"}	0	0	d624364e-e997-430d-91ef-3ef0171a11fc			
2025-10-21 04:51:38.132718+09	2025-10-21 04:51:38.132733+09	92d3e996-a574-4708-9581-877a7c78d3cf	GLI Premium 후드티	프리미엄 코튼 소재의 GLI 브랜드 후드티입니다. 부드럽고 따뜻한 착용감과 세련된 디자인이 특징입니다.	GLI 브랜드 프리미엄 코튼 후드티	goods	89.99000000	89.99	15	t	https://placehold.co/400x500/000000/D4AF37/png?text=GLI+Hoodie	[]	active	t	["패션", "의류", "후드티", "프리미엄", "Fashion", "Clothing", "Hoodie", "Premium"]	{"sizes": ["S", "M", "L", "XL"], "colors": ["Black", "Navy", "Gray"], "material": "Premium Cotton", "categoryId": "fashion", "salePercent": 25, "originalPrice": 120.0}	0	0	04617999-d1c9-4a59-b688-546211820c45			
2025-10-21 04:51:38.139924+09	2025-10-21 04:51:38.139944+09	926ba515-4a65-454c-be86-2af90989c3b7	GLI Signature 모자	GLI 로고가 새겨진 시그니처 캡입니다. 어떤 스타일에도 잘 어울리는 베이직한 디자인입니다.	GLI 로고 시그니처 캡	goods	35.50000000	35.50	8	t	https://placehold.co/400x400/FFFFFF/000000/png?text=GLI+Cap	[]	active	f	["액세서리", "모자", "캡", "Accessories", "Hat", "Cap"]	{"colors": ["Black", "White", "Navy"], "adjustable": true, "categoryId": "accessories"}	0	0	04617999-d1c9-4a59-b688-546211820c45			
2025-10-21 04:51:38.147315+09	2025-10-21 04:51:38.147329+09	b2509b04-9f03-45e2-9e48-d30559f0d67a	GLI 무선 이어폰	고음질 GLI 브랜드 블루투스 이어폰입니다. 최신 노이즈 캔슬링 기술과 긴 배터리 수명을 자랑합니다.	고음질 블루투스 이어폰	goods	149.99000000	149.99	12	t	https://placehold.co/400x400/1E90FF/FFFFFF/png?text=GLI+Earphones	[]	active	t	["전자기기", "이어폰", "블루투스", "Electronics", "Earphones", "Bluetooth"]	{"categoryId": "electronics", "waterproof": "IPX4", "batteryLife": "24 hours", "salePercent": 25, "originalPrice": 199.99, "noiseCanceling": true}	0	0	04617999-d1c9-4a59-b688-546211820c45			
2025-10-21 04:51:38.154635+09	2025-10-21 04:51:38.15465+09	eb8ac98f-8b7a-4566-872a-5a594cb3918f	GLI 텀블러	보온/보냉 기능이 있는 GLI 브랜드 텀블러입니다. 스테인레스 스틸 소재로 오래도록 사용할 수 있습니다.	보온/보냉 스테인레스 텀블러	goods	25.00000000	25.00	20	t	https://placehold.co/300x500/C0C0C0/000000/png?text=GLI+Tumbler	[]	active	f	["라이프스타일", "텀블러", "스테인레스", "Lifestyle", "Tumbler", "Stainless"]	{"colors": ["Silver", "Black", "Gold"], "capacity": "500ml", "material": "Stainless Steel", "categoryId": "lifestyle"}	0	0	04617999-d1c9-4a59-b688-546211820c45			
2025-10-21 04:51:38.170475+09	2025-10-21 04:51:38.170488+09	db7f4e92-d2b8-4e30-a94c-0ae1da3af871	GLI 디퓨저	GLI 시그니처 향이 나는 아로마 디퓨저입니다. 고급스러운 디자인과 은은한 향으로 공간을 채워줍니다.	GLI 시그니처 향 아로마 디퓨저	goods	95.00000000	95.00	0	t	https://placehold.co/400x500/FFD700/000000/png?text=GLI+Diffuser	[]	active	f	["홈&리빙", "디퓨저", "향", "인테리어", "Home", "Diffuser", "Fragrance", "Interior"]	{"scents": ["Lavender", "Ocean Breeze", "Forest"], "capacity": "200ml", "duration": "60 days", "categoryId": "home"}	0	0	04617999-d1c9-4a59-b688-546211820c45			
2025-10-21 04:51:38.178975+09	2025-10-21 04:51:38.178994+09	c69e649a-2167-4f9d-a2ad-30becdb9d0c8	GLI 스마트워치	GLI 브랜딩이 적용된 스마트워치입니다. 건강 관리와 스마트 기능이 완벽하게 조화를 이룹니다.	GLI 브랜딩 스마트워치	goods	299.99000000	299.99	5	t	https://placehold.co/400x400/000000/1E90FF/png?text=GLI+Watch	[]	active	t	["전자기기", "스마트워치", "웨어러블", "Electronics", "Smart Watch", "Wearable"]	{"features": ["Heart Rate Monitor", "GPS", "Sleep Tracking", "Notification"], "categoryId": "electronics", "waterproof": "5ATM", "batteryLife": "5 days", "compatibility": ["iOS", "Android"]}	0	0	04617999-d1c9-4a59-b688-546211820c45			
2025-10-21 04:51:38.185095+09	2025-10-21 04:51:38.185109+09	36d20958-cf31-49b8-a02f-3315197e42a3	GLI 레더 지갑	프리미엄 가죽으로 제작된 GLI 지갑입니다. 실용적인 디자인과 고급스러운 마감이 특징입니다.	프리미엄 가죽 지갑	goods	128.00000000	128.00	10	t	https://placehold.co/400x300/8B4513/FFFFFF/png?text=GLI+Wallet	[]	active	f	["액세서리", "지갑", "가죽", "Accessories", "Wallet", "Leather"]	{"colors": ["Black", "Brown", "Navy"], "material": "Genuine Leather", "cardSlots": 8, "categoryId": "accessories", "salePercent": 20, "originalPrice": 160.0}	0	0	04617999-d1c9-4a59-b688-546211820c45			
2025-10-21 04:51:38.190748+09	2025-10-21 04:51:38.190761+09	2cfb3974-e80f-4c33-ad49-3e8a86af6d11	GLI Fine Dining Seoul	서울 강남에 위치한 프렌치 파인 다이닝 레스토랑입니다. 미슐랭 스타 셰프가 선보이는 혁신적인 요리를 경험하세요.	미슐랭 스타 프렌치 파인 다이닝	restaurant	200.00000000	200.00	30	t	https://placehold.co/800x600/800020/FFFFFF/png?text=GLI+Fine+Dining	[]	active	t	["파인다이닝", "프렌치", "미슐랭", "강남", "Fine Dining", "French", "Michelin", "Gangnam"]	{"courses": [{"name": "런치 코스", "price": 150, "name_en": "Lunch Course", "description": "5코스 런치 메뉴", "description_en": "5-course lunch menu"}, {"name": "디너 코스", "price": 200, "name_en": "Dinner Course", "description": "7코스 디너 메뉴", "description_en": "7-course dinner menu"}, {"name": "시그니처 코스", "price": 350, "name_en": "Signature Course", "description": "10코스 시그니처 메뉴", "description_en": "10-course signature menu"}], "cuisine": "French", "location": "Gangnam, Seoul", "dress_code": "Business Casual", "location_en": "Gangnam, Seoul", "price_range": "₩₩₩₩", "business_hours": {"lunch": "12:00 - 15:00", "dinner": "18:00 - 22:00"}, "michelin_stars": 2}	0	0	7440548d-5680-4b9f-b930-42aad4a8a638			
2025-10-21 04:51:38.197672+09	2025-10-21 04:51:38.197685+09	2b008353-654a-4772-a30c-26250df830d8	GLI Japanese Omakase	청담동에 위치한 정통 일식 오마카세 레스토랑입니다. 당일 공수한 신선한 재료로 최고의 스시를 선보입니다.	정통 일식 오마카세	restaurant	250.00000000	250.00	20	t	https://placehold.co/800x600/DC143C/FFFFFF/png?text=GLI+Omakase	[]	active	t	["일식", "오마카세", "스시", "청담동", "Japanese", "Omakase", "Sushi", "Cheongdam"]	{"courses": [{"name": "스탠다드 오마카세", "price": 250, "name_en": "Standard Omakase", "description": "15피스 니기리", "description_en": "15-piece nigiri"}, {"name": "프리미엄 오마카세", "price": 400, "name_en": "Premium Omakase", "description": "20피스 니기리 + 특선 요리", "description_en": "20-piece nigiri + special dishes"}], "cuisine": "Japanese", "seating": "Counter only (12 seats)", "location": "Cheongdam-dong, Seoul", "location_en": "Cheongdam-dong, Seoul", "price_range": "₩₩₩₩₩", "reservations": "Required", "business_hours": {"lunch": "By reservation only", "dinner": "18:00 - 22:00"}}	0	0	7440548d-5680-4b9f-b930-42aad4a8a638			
2025-10-21 04:51:38.203588+09	2025-10-21 04:51:38.203601+09	edbfb793-7c22-4e72-bbdd-0754cf65a9ba	GLI Italian Trattoria	이태원에 위치한 정통 이탈리안 트라토리아입니다. 전통 레시피와 신선한 재료로 진정한 이탈리아의 맛을 선사합니다.	정통 이탈리안 트라토리아	restaurant	120.00000000	120.00	40	t	https://placehold.co/800x600/008000/FFFFFF/png?text=GLI+Trattoria	[]	active	t	["이탈리안", "파스타", "피자", "이태원", "Italian", "Pasta", "Pizza", "Itaewon"]	{"cuisine": "Italian", "ambiance": "Casual", "location": "Itaewon, Seoul", "location_en": "Itaewon, Seoul", "price_range": "₩₩₩", "specialties": ["Handmade Pasta", "Wood-fired Pizza", "Tiramisu"], "business_hours": {"lunch": "11:30 - 15:00", "dinner": "17:30 - 22:00"}, "menu_highlights": [{"name": "트러플 파스타", "price": 45, "name_en": "Truffle Pasta"}, {"name": "마르게리타 피자", "price": 28, "name_en": "Margherita Pizza"}, {"name": "오쏘부코", "price": 55, "name_en": "Osso Buco"}]}	0	0	7440548d-5680-4b9f-b930-42aad4a8a638			
\.


--
-- Data for Name: solana_transactions; Type: TABLE DATA; Schema: public; Owner: gli
--

COPY public.solana_transactions (id, transaction_hash, transaction_type, amount, status, created_at, confirmed_at, user_id) FROM stdin;
\.


--
-- Data for Name: solana_users; Type: TABLE DATA; Schema: public; Owner: gli
--

COPY public.solana_users (password, is_superuser, is_staff, date_joined, id, wallet_address, username, email, first_name, last_name, membership_level, sol_balance, last_balance_update, is_active, created_at, updated_at, last_login, vpx_experience, vpx_partner, vpx_verify) FROM stdin;
pbkdf2_sha256$720000$OwFtuSRXleVbpBD3SsvnfE$QhbFzy4AqoNl0WF3xHhhundqX10vkmhfMs8VLgUaJCA=	t	t	2025-10-13 23:56:55.102+09	03129597-8698-473b-bc65-9569b04b856f	\N	admin_gli	admin@gli.com	GLI	Administrator	vip	0.000000000	2025-10-13 23:56:55.103+09	t	2025-10-13 23:56:55.103+09	2025-10-13 23:56:55.103+09	\N	0	0	1
pbkdf2_sha256$720000$30ROgAwwx1Ebzd80xuMPyp$AAFDMdtJvXAOvllFhCLu3HV8CVE5rxTV5vt7e0Xocq4=	f	t	2025-10-13 23:56:55.112+09	25b34ad5-ddc0-41bc-a35d-2c3de28e22c9	m2WLvPZ5MdZ5LczEN2dhAnJmSXyn9M5tp5wYyevHA2KF	token_manager	token@gli.com	Token	Manager	premium	0.000000000	2025-10-13 23:56:55.113+09	t	2025-10-13 23:56:55.113+09	2025-10-13 23:56:55.113+09	\N	0	0	1
pbkdf2_sha256$720000$1ph5z5wQTU4Z1jsjHK8Fna$VLf7nYtIwyUTX4lzCL+qFRkUvo9Ovqn3zZWDTQK16Bw=	t	t	2025-10-13 23:56:55.117+09	2dd24951-db0a-49b7-9dcb-47f06a366fca	\N	ahndong	ahndong@user.gli.com			premium	0.000000000	2025-10-13 23:56:55.117+09	t	2025-10-13 23:56:55.117+09	2025-10-13 23:56:55.117+09	\N	0	0	1
pbkdf2_sha256$720000$hhIgYlopJG2PdL9UzOlj8c$40dZ9PqS0XVmDeRZS/xLXUTlD2WeWqqN1NVOkca3xK8=	f	t	2025-10-13 23:56:55.121+09	513bd8bd-bfdd-4c41-9062-06a93beec771	\N	admin1	admin1@gli.com	일반	관리자1	premium	0.000000000	2025-10-14 00:01:08.548+09	t	2025-10-13 23:56:55.121+09	2025-10-14 00:01:08.548+09	2025-10-14 00:01:08.547+09	0	0	1
pbkdf2_sha256$720000$Lq559WTMmxdsyDfCElqk1a$RyO/ThPMB52QGTt3IL7S47YXOJn3GyDtR74o19OJHv8=	f	f	2025-10-13 23:56:55.138+09	a24eec0b-88dd-401d-b8f6-d2ec9b9b63b9	qXNam8PzsgVrvXVi4KX2aTNcjYUHCobAd47yhWcN4RDV	member3	member3@gli.com	회원	3	basic	0.000000000	2025-10-13 23:56:55.138+09	t	2025-10-13 23:56:55.139+09	2025-10-13 23:56:55.139+09	\N	0	0	1
pbkdf2_sha256$720000$goJoVIskahfOz2VogUIZ9H$1d8vPohsaz2GFzG7Kd46apgxjD1XjxfR4ueI/GH5H/E=	f	t	2025-10-13 23:56:55.143+09	b50c4ed5-c11f-41fc-966f-83d0736683d1	\N	admin2	admin2@gli.com	일반	관리자2	premium	0.000000000	2025-10-13 23:56:55.143+09	t	2025-10-13 23:56:55.143+09	2025-10-13 23:56:55.143+09	\N	0	0	1
pbkdf2_sha256$720000$EkTPGJAibDkhhso2vSaMQE$nUXyRRfEVGHoh5opkuO7Su6BMbYYMQgoghxQOsolrTw=	t	t	2025-10-13 23:56:55.134+09	7d6c5a92-d357-45a6-a533-6eb47c3af5d7	\N	superadmin2	superadmin2@gli.com	슈퍼	관리자2	premium	0.000000000	2025-10-21 05:03:28.19923+09	t	2025-10-13 23:56:55.135+09	2025-10-21 05:03:28.199248+09	2025-10-21 05:03:28.199082+09	0	0	1
pbkdf2_sha256$720000$zpnNHh32xyW0UF5iWZYwmJ$AsFntTzY8uzvNZr4DY06FoD8j0jlx58R2wN/OcuZmmg=	f	f	2025-10-13 23:56:55.108+09	043da7d2-a85f-4d33-8059-5df077ca80a2	5utTkSwBzqhwMRYF71S7pu17gcBU6M53UrwS3JquRtgg	member2	member2@gli.com	회원	2	premium	0.000000000	2025-10-21 05:15:31.203534+09	t	2025-10-13 23:56:55.108+09	2025-10-21 05:15:31.203551+09	2025-10-21 05:15:31.203406+09	0	0	1
pbkdf2_sha256$720000$WaaKIPnRjLZfUh82u3ABOn$j+A5FVkODdQ1QYpUV9AHKziMS1eYUlDXbwPUFqVEyJg=	f	f	2025-10-13 23:56:55.125+09	5b244624-8cb4-4645-94e6-95d71d365110	5rFHPQ62n6f7dTJRwvuEzjLrvgYtRyfuimnnnm7FTug6	member1	member1@gli.com	회원	1	premium	0.000000000	2025-10-21 01:55:01.326873+09	t	2025-10-13 23:56:55.125+09	2025-10-21 01:55:01.326897+09	2025-10-21 01:55:01.32665+09	0	0	1
pbkdf2_sha256$720000$hxTSYyiyWa1e2M81IAYacx$0siJe4I2wEDOfO85c9Vic22mgjn34TqHicWuroJuHvA=	t	t	2025-10-13 23:56:55.129+09	6da4715f-dee9-4821-8c39-6310f46250b3	\N	superadmin1	superadmin1@gli.com	슈퍼	관리자1	premium	0.000000000	2025-10-21 15:43:18.467126+09	t	2025-10-13 23:56:55.13+09	2025-10-21 15:43:18.467148+09	2025-10-21 15:43:18.466904+09	0	0	1
\.


--
-- Data for Name: solana_users_groups; Type: TABLE DATA; Schema: public; Owner: gli
--

COPY public.solana_users_groups (id, solanauser_id, group_id) FROM stdin;
\.


--
-- Data for Name: solana_users_user_permissions; Type: TABLE DATA; Schema: public; Owner: gli
--

COPY public.solana_users_user_permissions (id, solanauser_id, permission_id) FROM stdin;
\.


--
-- Data for Name: strategy_phases; Type: TABLE DATA; Schema: public; Owner: gli
--

COPY public.strategy_phases (id, icon, title_ko, title_en, description_ko, description_en, features_ko, "order", is_active, created_at, updated_at, features_en) FROM stdin;
550565fb-392b-4a35-aba4-45e6527b87cb	🪙	실물자산 토큰화 (RWA)	Real-World Asset Tokenization	실물자산 토큰(RWA) 운용을 통해 안정적인 수익 기반을 확보하고 초기 투자 생태계를 형성합니다.	Secure stable returns through real-world asset (RWA) token operations and establish the initial investment ecosystem.	["부동산·리조트 RWA 토큰 발행", "실물 담보 기반 운용 모델", "안정형 투자 상품 출시"]	0	t	2025-10-21 00:40:09.534224+09	2025-10-21 00:40:09.534237+09	["Real estate and resort RWA token issuance", "Asset-backed operation model", "Launch of stable investment products"]
4826c574-a7c7-4927-99f2-b24f595b6e48	🌐	글로벌 커뮤니티 확장	Global Community Expansion	글로벌 여행·레저 플랫폼 기반의 토큰 커뮤니티를 구축하고, 브랜드 마케팅 파워를 강화합니다.	Build a token-based global community around travel and leisure platforms and enhance brand marketing power.	["글로벌 레저 파트너십 구축", "커뮤니티 리워드 프로그램", "마케팅 DAO 운영"]	1	t	2025-10-21 00:40:09.537797+09	2025-10-21 00:40:09.537807+09	["Global leisure partnerships", "Community reward programs", "Marketing DAO operations"]
baa65be7-1c04-49a4-8dc1-acf9160a2c6b	💱	라이선스 기반 디지털 자산 거래소 설립	Licensed Digital Asset Exchange	GLI 생태계를 연결하는 허브로서, STO와 가상자산을 아우르는 거래소를 설립하여 DeFi 인프라를 확장합니다.	Establish a licensed exchange connecting GLI's ecosystem, integrating STO and crypto markets to expand DeFi infrastructure.	["STO 및 가상자산 상장", "규제 대응형 거래 시스템", "온·오프체인 연동 결제 시스템"]	2	t	2025-10-21 00:40:09.541088+09	2025-10-21 00:40:09.541099+09	["STO and crypto listings", "Regulatory-compliant trading system", "On-chain/off-chain payment integration"]
83cf2d39-e9e7-4d86-b22b-2b847c0712aa	🎰	소셜 카지노 플랫폼 확장	Social Casino Platform Expansion	소셜 카지노와 레저 플랫폼의 결합을 통해 수익성과 이용자 참여를 극대화하고, 매출 1천억 원 달성을 목표로 합니다.	Combine social casino and leisure platforms to maximize profitability and user engagement, targeting KRW 100 billion in revenue.	["카지노 게임·NFT 연동", "크로스체인 결제 시스템", "유저 랭킹 및 리워드 구조"]	3	t	2025-10-21 00:40:09.543952+09	2025-10-21 00:40:09.543962+09	["Casino games integrated with NFTs", "Cross-chain payment system", "User ranking and reward mechanisms"]
530400e9-81da-4c6e-9e8c-84623cf0963c	🚀	글로벌 상장 및 지속 성장	Global Listing and Sustainable Growth	소셜 카지노 게임사로서 지속적인 성장 기반을 마련하고, 북미 시장 중심으로 나스닥 상장을 추진합니다.	Build a foundation for sustainable growth as a social gaming company and pursue NASDAQ listing in North America.	["북미 시장 진출", "글로벌 상장 준비 및 IR 강화", "지속 가능한 Web3 비즈니스 모델 확립"]	4	t	2025-10-21 00:40:09.546708+09	2025-10-21 00:40:09.546717+09	["Expansion into North American markets", "IPO readiness and investor relations", "Establish sustainable Web3 business model"]
\.


--
-- Data for Name: team_members; Type: TABLE DATA; Schema: public; Owner: gli
--

COPY public.team_members (id, image_url, position_ko, position_en, role_ko, role_en, tags, "order", is_active, created_at, updated_at, name_en, name_ko) FROM stdin;
37cd12fe-51e7-4f54-ade4-448674128b8d	https://gli-platform-media-staging.s3.ap-northeast-2.amazonaws.com/test-api-upload/443425cc97924e4e86ce4da27c71777b_20251020_112104.png	테스트 직책	Test Position	테스트 역할	Test Role	["test", "api"]	999	t	2025-10-20 11:21:04.471+09	2025-10-20 12:40:46.548+09	Not Entered	미입력
7a17eb85-4738-4451-8e1c-8d21e0f42140	\N	테스트 CEO	Test CEO	GLI Platform 테스트를 담당합니다.	Responsible for GLI Platform testing.	["Testing", "Quality Assurance", "Development"]	99	t	2025-10-20 13:18:23.351+09	2025-10-20 13:21:14.943+09	Not Entered	미입력
98ebcd9b-96ab-4f8c-be0b-39e849064309	https://gli-platform-media-staging.s3.ap-northeast-2.amazonaws.com/business-content/64ef8ed09dae4f01a0fad7c34b573517_20251020_132135.png	CTO - IT 총괄	CTO	테스트 역할	Test Role	["test", "api"]	999	t	2025-10-20 12:44:49.569+09	2025-10-20 14:01:44.227+09	Dr. MannerTone	닥터메너톤
d72a04ea-3f7f-4318-9cd9-5d5b77841119	https://gli-platform-media-staging.s3.ap-northeast-2.amazonaws.com/test-api-upload/92859467962647ceae63271e3b9c7d8d_20251020_123508.png	테스트 직책	Test Position	테스트 역할	Test Role	["test", "api"]	999	t	2025-10-20 12:35:08.901+09	2025-10-20 12:35:08.901+09	Not Entered	미입력
f879c0b5-14c5-46a8-9cc7-a85ceb44d967	\N	GLI CEO	Chief Executive Officer	GLI Platform의 전반적인 운영과 전략적 방향을 담당합니다.	Responsible for overall operations and strategic direction of GLI Platform.	["Leadership", "Strategy", "Blockchain"]	1	t	2025-10-20 13:30:50.451+09	2025-10-20 13:30:50.452+09	GLI Kim	김GLI
fa0b2af5-242b-450d-b1b0-22d0cb752573	\N	테스트 직책	Test Position	테스트 역할	Test Role	["test", "api"]	999	t	2025-10-20 12:45:45.915+09	2025-10-20 13:21:22.616+09	Not Entered	미입력
\.


--
-- Data for Name: token_ecosystems; Type: TABLE DATA; Schema: public; Owner: gli
--

COPY public.token_ecosystems (id, icon, name, symbol, description_ko, description_en, total_supply, current_price, "order", is_active, created_at, updated_at, features_en, features_ko) FROM stdin;
81564211-d453-404b-a818-ef4a5890f10c	🔵	GLI Business	GLIB	GLIB는 실물자산 기반의 투자형 코인으로, 동남아 부동산 및 사업 아이템에 투자됩니다.\n수익률에 따른 배당이 제공되며, 거래소 상장 계획은 없고, 일정 등급 이상의 보유자에게 주식매수권이 부여됩니다.	GLIB is a real-asset investment token for Southeast Asian real estate and business ventures.\nHolders receive dividends based on performance; no exchange listing is planned. High-tier holders may be granted stock purchase rights.	1,000,000,000	$1	1	t	2025-10-21 01:37:58.263365+09	2025-10-21 01:37:58.26338+09	["Purchase via presale", "Dividend distribution by yield", "No exchange listing plan", "Tiered benefits by holding volume", "Stock purchase rights granted"]	["프리세일을 통해 구매", "수익률에 따른 배당", "거래소 상장 계획 없음", "등급 및 보유량에 따라 혜택 차등", "주식매수권 부여"]
a211269a-9043-4544-9261-fde5bbd21087	🔷	GLI Governance	GLID	GLID는 플랫폼의 의사결정과 운영 투표에 참여할 수 있는 거버넌스 코인입니다.\n투자 사업 아이템 및 중개 서비스 수수료 지불에 활용되며, 거래소 상장 가능한 주요 유통 토큰입니다.	GLID is a governance token enabling participation in platform voting and decision-making.\nUsed for investment project voting and service fee payments. It serves as a tradable exchange-listed governance asset.	500,000,000	$0.8	2	t	2025-10-21 01:37:58.267365+09	2025-10-21 01:37:58.267377+09	["Participate in investment project voting", "Pay brokerage and service fees", "Review investment portfolios", "Evaluate business schedules and priorities", "Exchange-listed governance token"]	["투자 사업 아이템 투표 참여", "중개 서비스 수수료 지불", "투자 포트폴리오 검토", "사업 일정 및 순위 검토", "거래소 상장 토큰"]
f2b0454b-7a3d-4968-9b5c-13c19d0e4a88	🔹	GLI Leisure	GLIL	GLIL은 오프체인에서 사용되는 게임 및 레저 포인트로, 동남아 레저 상품 이용에 사용됩니다.\n현금 전환이 불가하며, 미화 달러에 1:1 페깅되어 GLI 플랫폼 내에서만 교환 가능합니다.	GLIL is an off-chain game and leisure point used for Southeast Asian leisure services.\nIt is non-convertible to cash, pegged 1:1 with USD, and exchangeable only within the GLI platform.	2,000,000,000	$1	3	t	2025-10-21 01:37:58.269257+09	2025-10-21 01:37:58.269267+09	["Used within the gaming ecosystem", "Not convertible to cash", "Pegged 1:1 to USD", "No listing or sale plan", "Exchangeable within GLI platform"]	["게임 생태계 전용 포인트", "현금 환전 불가", "미화 달러 1:1 페깅", "상장 및 세일 계획 없음", "GLI 플랫폼 내 교환 가능"]
\.


--
-- Name: admin_grades_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gli
--

SELECT pg_catalog.setval('public.admin_grades_id_seq', 2, true);


--
-- Name: admin_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gli
--

SELECT pg_catalog.setval('public.admin_permissions_id_seq', 1, false);


--
-- Name: admin_users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gli
--

SELECT pg_catalog.setval('public.admin_users_id_seq', 7, true);


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gli
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gli
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_nonces_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gli
--

SELECT pg_catalog.setval('public.auth_nonces_id_seq', 1, true);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gli
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 96, true);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gli
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 1, false);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gli
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 24, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gli
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 33, true);


--
-- Name: grade_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gli
--

SELECT pg_catalog.setval('public.grade_permissions_id_seq', 1, false);


--
-- Name: solana_transactions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gli
--

SELECT pg_catalog.setval('public.solana_transactions_id_seq', 1, false);


--
-- Name: solana_users_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gli
--

SELECT pg_catalog.setval('public.solana_users_groups_id_seq', 1, false);


--
-- Name: solana_users_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gli
--

SELECT pg_catalog.setval('public.solana_users_user_permissions_id_seq', 1, false);


--
-- Name: admin_grades admin_grades_name_key; Type: CONSTRAINT; Schema: public; Owner: gli
--

ALTER TABLE ONLY public.admin_grades
    ADD CONSTRAINT admin_grades_name_key UNIQUE (name);


--
-- Name: admin_grades admin_grades_pkey; Type: CONSTRAINT; Schema: public; Owner: gli
--

ALTER TABLE ONLY public.admin_grades
    ADD CONSTRAINT admin_grades_pkey PRIMARY KEY (id);


--
-- Name: admin_permissions admin_permissions_codename_key; Type: CONSTRAINT; Schema: public; Owner: gli
--

ALTER TABLE ONLY public.admin_permissions
    ADD CONSTRAINT admin_permissions_codename_key UNIQUE (codename);


--
-- Name: admin_permissions admin_permissions_name_key; Type: CONSTRAINT; Schema: public; Owner: gli
--

ALTER TABLE ONLY public.admin_permissions
    ADD CONSTRAINT admin_permissions_name_key UNIQUE (name);


--
-- Name: admin_permissions admin_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: gli
--

ALTER TABLE ONLY public.admin_permissions
    ADD CONSTRAINT admin_permissions_pkey PRIMARY KEY (id);


--
-- Name: admin_users admin_users_pkey; Type: CONSTRAINT; Schema: public; Owner: gli
--

ALTER TABLE ONLY public.admin_users
    ADD CONSTRAINT admin_users_pkey PRIMARY KEY (id);


--
-- Name: admin_users admin_users_user_id_key; Type: CONSTRAINT; Schema: public; Owner: gli
--

ALTER TABLE ONLY public.admin_users
    ADD CONSTRAINT admin_users_user_id_key UNIQUE (user_id);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: gli
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: gli
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: gli
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: gli
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_nonces auth_nonces_nonce_key; Type: CONSTRAINT; Schema: public; Owner: gli
--

ALTER TABLE ONLY public.auth_nonces
    ADD CONSTRAINT auth_nonces_nonce_key UNIQUE (nonce);


--
-- Name: auth_nonces auth_nonces_pkey; Type: CONSTRAINT; Schema: public; Owner: gli
--

ALTER TABLE ONLY public.auth_nonces
    ADD CONSTRAINT auth_nonces_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: gli
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: gli
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: business_contents business_contents_pkey; Type: CONSTRAINT; Schema: public; Owner: gli
--

ALTER TABLE ONLY public.business_contents
    ADD CONSTRAINT business_contents_pkey PRIMARY KEY (id);


--
-- Name: business_contents business_contents_section_order_5ecbff5d_uniq; Type: CONSTRAINT; Schema: public; Owner: gli
--

ALTER TABLE ONLY public.business_contents
    ADD CONSTRAINT business_contents_section_order_5ecbff5d_uniq UNIQUE (section, "order");


--
-- Name: development_timelines development_timelines_pkey; Type: CONSTRAINT; Schema: public; Owner: gli
--

ALTER TABLE ONLY public.development_timelines
    ADD CONSTRAINT development_timelines_pkey PRIMARY KEY (id);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: gli
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: gli
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: gli
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: gli
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: gli
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: face_verifications face_verifications_pkey; Type: CONSTRAINT; Schema: public; Owner: gli
--

ALTER TABLE ONLY public.face_verifications
    ADD CONSTRAINT face_verifications_pkey PRIMARY KEY (id);


--
-- Name: grade_permissions grade_permissions_grade_id_permission_id_7b6d0f61_uniq; Type: CONSTRAINT; Schema: public; Owner: gli
--

ALTER TABLE ONLY public.grade_permissions
    ADD CONSTRAINT grade_permissions_grade_id_permission_id_7b6d0f61_uniq UNIQUE (grade_id, permission_id);


--
-- Name: grade_permissions grade_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: gli
--

ALTER TABLE ONLY public.grade_permissions
    ADD CONSTRAINT grade_permissions_pkey PRIMARY KEY (id);


--
-- Name: investments investments_pkey; Type: CONSTRAINT; Schema: public; Owner: gli
--

ALTER TABLE ONLY public.investments
    ADD CONSTRAINT investments_pkey PRIMARY KEY (id);


--
-- Name: project_features project_features_pkey; Type: CONSTRAINT; Schema: public; Owner: gli
--

ALTER TABLE ONLY public.project_features
    ADD CONSTRAINT project_features_pkey PRIMARY KEY (id);


--
-- Name: rwa_assets rwa_assets_pkey; Type: CONSTRAINT; Schema: public; Owner: gli
--

ALTER TABLE ONLY public.rwa_assets
    ADD CONSTRAINT rwa_assets_pkey PRIMARY KEY (id);


--
-- Name: rwa_categories rwa_categories_name_key; Type: CONSTRAINT; Schema: public; Owner: gli
--

ALTER TABLE ONLY public.rwa_categories
    ADD CONSTRAINT rwa_categories_name_key UNIQUE (name);


--
-- Name: rwa_categories rwa_categories_pkey; Type: CONSTRAINT; Schema: public; Owner: gli
--

ALTER TABLE ONLY public.rwa_categories
    ADD CONSTRAINT rwa_categories_pkey PRIMARY KEY (id);


--
-- Name: shopping_categories shopping_categories_name_key; Type: CONSTRAINT; Schema: public; Owner: gli
--

ALTER TABLE ONLY public.shopping_categories
    ADD CONSTRAINT shopping_categories_name_key UNIQUE (name);


--
-- Name: shopping_categories shopping_categories_pkey; Type: CONSTRAINT; Schema: public; Owner: gli
--

ALTER TABLE ONLY public.shopping_categories
    ADD CONSTRAINT shopping_categories_pkey PRIMARY KEY (id);


--
-- Name: shopping_order_items shopping_order_items_pkey; Type: CONSTRAINT; Schema: public; Owner: gli
--

ALTER TABLE ONLY public.shopping_order_items
    ADD CONSTRAINT shopping_order_items_pkey PRIMARY KEY (id);


--
-- Name: shopping_orders shopping_orders_order_number_key; Type: CONSTRAINT; Schema: public; Owner: gli
--

ALTER TABLE ONLY public.shopping_orders
    ADD CONSTRAINT shopping_orders_order_number_key UNIQUE (order_number);


--
-- Name: shopping_orders shopping_orders_pkey; Type: CONSTRAINT; Schema: public; Owner: gli
--

ALTER TABLE ONLY public.shopping_orders
    ADD CONSTRAINT shopping_orders_pkey PRIMARY KEY (id);


--
-- Name: shopping_products shopping_products_pkey; Type: CONSTRAINT; Schema: public; Owner: gli
--

ALTER TABLE ONLY public.shopping_products
    ADD CONSTRAINT shopping_products_pkey PRIMARY KEY (id);


--
-- Name: solana_transactions solana_transactions_pkey; Type: CONSTRAINT; Schema: public; Owner: gli
--

ALTER TABLE ONLY public.solana_transactions
    ADD CONSTRAINT solana_transactions_pkey PRIMARY KEY (id);


--
-- Name: solana_transactions solana_transactions_transaction_hash_key; Type: CONSTRAINT; Schema: public; Owner: gli
--

ALTER TABLE ONLY public.solana_transactions
    ADD CONSTRAINT solana_transactions_transaction_hash_key UNIQUE (transaction_hash);


--
-- Name: solana_users_groups solana_users_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: gli
--

ALTER TABLE ONLY public.solana_users_groups
    ADD CONSTRAINT solana_users_groups_pkey PRIMARY KEY (id);


--
-- Name: solana_users_groups solana_users_groups_solanauser_id_group_id_bf859b19_uniq; Type: CONSTRAINT; Schema: public; Owner: gli
--

ALTER TABLE ONLY public.solana_users_groups
    ADD CONSTRAINT solana_users_groups_solanauser_id_group_id_bf859b19_uniq UNIQUE (solanauser_id, group_id);


--
-- Name: solana_users solana_users_pkey; Type: CONSTRAINT; Schema: public; Owner: gli
--

ALTER TABLE ONLY public.solana_users
    ADD CONSTRAINT solana_users_pkey PRIMARY KEY (id);


--
-- Name: solana_users_user_permissions solana_users_user_permis_solanauser_id_permission_75f6ca92_uniq; Type: CONSTRAINT; Schema: public; Owner: gli
--

ALTER TABLE ONLY public.solana_users_user_permissions
    ADD CONSTRAINT solana_users_user_permis_solanauser_id_permission_75f6ca92_uniq UNIQUE (solanauser_id, permission_id);


--
-- Name: solana_users_user_permissions solana_users_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: gli
--

ALTER TABLE ONLY public.solana_users_user_permissions
    ADD CONSTRAINT solana_users_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: solana_users solana_users_username_key; Type: CONSTRAINT; Schema: public; Owner: gli
--

ALTER TABLE ONLY public.solana_users
    ADD CONSTRAINT solana_users_username_key UNIQUE (username);


--
-- Name: solana_users solana_users_wallet_address_key; Type: CONSTRAINT; Schema: public; Owner: gli
--

ALTER TABLE ONLY public.solana_users
    ADD CONSTRAINT solana_users_wallet_address_key UNIQUE (wallet_address);


--
-- Name: strategy_phases strategy_phases_pkey; Type: CONSTRAINT; Schema: public; Owner: gli
--

ALTER TABLE ONLY public.strategy_phases
    ADD CONSTRAINT strategy_phases_pkey PRIMARY KEY (id);


--
-- Name: team_members team_members_pkey; Type: CONSTRAINT; Schema: public; Owner: gli
--

ALTER TABLE ONLY public.team_members
    ADD CONSTRAINT team_members_pkey PRIMARY KEY (id);


--
-- Name: token_ecosystems token_ecosystems_pkey; Type: CONSTRAINT; Schema: public; Owner: gli
--

ALTER TABLE ONLY public.token_ecosystems
    ADD CONSTRAINT token_ecosystems_pkey PRIMARY KEY (id);


--
-- Name: admin_grades_name_8af46b3c_like; Type: INDEX; Schema: public; Owner: gli
--

CREATE INDEX admin_grades_name_8af46b3c_like ON public.admin_grades USING btree (name varchar_pattern_ops);


--
-- Name: admin_permissions_codename_41bf9c7e_like; Type: INDEX; Schema: public; Owner: gli
--

CREATE INDEX admin_permissions_codename_41bf9c7e_like ON public.admin_permissions USING btree (codename varchar_pattern_ops);


--
-- Name: admin_permissions_name_01494afb_like; Type: INDEX; Schema: public; Owner: gli
--

CREATE INDEX admin_permissions_name_01494afb_like ON public.admin_permissions USING btree (name varchar_pattern_ops);


--
-- Name: admin_users_grade_id_d7e8ab63; Type: INDEX; Schema: public; Owner: gli
--

CREATE INDEX admin_users_grade_id_d7e8ab63 ON public.admin_users USING btree (grade_id);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: gli
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: gli
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: gli
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_nonces_nonce_ea70b2b7_like; Type: INDEX; Schema: public; Owner: gli
--

CREATE INDEX auth_nonces_nonce_ea70b2b7_like ON public.auth_nonces USING btree (nonce varchar_pattern_ops);


--
-- Name: auth_nonces_wallet_address_67e2508a; Type: INDEX; Schema: public; Owner: gli
--

CREATE INDEX auth_nonces_wallet_address_67e2508a ON public.auth_nonces USING btree (wallet_address);


--
-- Name: auth_nonces_wallet_address_67e2508a_like; Type: INDEX; Schema: public; Owner: gli
--

CREATE INDEX auth_nonces_wallet_address_67e2508a_like ON public.auth_nonces USING btree (wallet_address varchar_pattern_ops);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: gli
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- Name: business_contents_order_e9a2ea4e; Type: INDEX; Schema: public; Owner: gli
--

CREATE INDEX business_contents_order_e9a2ea4e ON public.business_contents USING btree ("order");


--
-- Name: business_contents_section_8db8dcc8; Type: INDEX; Schema: public; Owner: gli
--

CREATE INDEX business_contents_section_8db8dcc8 ON public.business_contents USING btree (section);


--
-- Name: business_contents_section_8db8dcc8_like; Type: INDEX; Schema: public; Owner: gli
--

CREATE INDEX business_contents_section_8db8dcc8_like ON public.business_contents USING btree (section varchar_pattern_ops);


--
-- Name: development_order_7b87e9_idx; Type: INDEX; Schema: public; Owner: gli
--

CREATE INDEX development_order_7b87e9_idx ON public.development_timelines USING btree ("order", is_active);


--
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: gli
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: gli
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: gli
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: gli
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: face_verifi_user_id_d95bf7_idx; Type: INDEX; Schema: public; Owner: gli
--

CREATE INDEX face_verifi_user_id_d95bf7_idx ON public.face_verifications USING btree (user_id, created_at DESC);


--
-- Name: face_verifi_verifie_9737b6_idx; Type: INDEX; Schema: public; Owner: gli
--

CREATE INDEX face_verifi_verifie_9737b6_idx ON public.face_verifications USING btree (verified, created_at DESC);


--
-- Name: face_verifications_user_id_e72defbc; Type: INDEX; Schema: public; Owner: gli
--

CREATE INDEX face_verifications_user_id_e72defbc ON public.face_verifications USING btree (user_id);


--
-- Name: grade_permissions_grade_id_59c9bf2e; Type: INDEX; Schema: public; Owner: gli
--

CREATE INDEX grade_permissions_grade_id_59c9bf2e ON public.grade_permissions USING btree (grade_id);


--
-- Name: grade_permissions_permission_id_f2072039; Type: INDEX; Schema: public; Owner: gli
--

CREATE INDEX grade_permissions_permission_id_f2072039 ON public.grade_permissions USING btree (permission_id);


--
-- Name: investments_investm_d1de42_idx; Type: INDEX; Schema: public; Owner: gli
--

CREATE INDEX investments_investm_d1de42_idx ON public.investments USING btree (investment_date DESC);


--
-- Name: investments_investo_49ded7_idx; Type: INDEX; Schema: public; Owner: gli
--

CREATE INDEX investments_investo_49ded7_idx ON public.investments USING btree (investor_id, status);


--
-- Name: investments_investor_id_96559232; Type: INDEX; Schema: public; Owner: gli
--

CREATE INDEX investments_investor_id_96559232 ON public.investments USING btree (investor_id);


--
-- Name: investments_rwa_ass_c871e4_idx; Type: INDEX; Schema: public; Owner: gli
--

CREATE INDEX investments_rwa_ass_c871e4_idx ON public.investments USING btree (rwa_asset_id, status);


--
-- Name: investments_rwa_asset_id_09fe90d8; Type: INDEX; Schema: public; Owner: gli
--

CREATE INDEX investments_rwa_asset_id_09fe90d8 ON public.investments USING btree (rwa_asset_id);


--
-- Name: project_fea_order_fc4473_idx; Type: INDEX; Schema: public; Owner: gli
--

CREATE INDEX project_fea_order_fc4473_idx ON public.project_features USING btree ("order", is_active);


--
-- Name: rwa_assets_categor_ed240e_idx; Type: INDEX; Schema: public; Owner: gli
--

CREATE INDEX rwa_assets_categor_ed240e_idx ON public.rwa_assets USING btree (category_id, status);


--
-- Name: rwa_assets_category_id_61d8811d; Type: INDEX; Schema: public; Owner: gli
--

CREATE INDEX rwa_assets_category_id_61d8811d ON public.rwa_assets USING btree (category_id);


--
-- Name: rwa_assets_is_feat_a378f2_idx; Type: INDEX; Schema: public; Owner: gli
--

CREATE INDEX rwa_assets_is_feat_a378f2_idx ON public.rwa_assets USING btree (is_featured DESC, created_at DESC);


--
-- Name: rwa_assets_risk_le_4b272a_idx; Type: INDEX; Schema: public; Owner: gli
--

CREATE INDEX rwa_assets_risk_le_4b272a_idx ON public.rwa_assets USING btree (risk_level, status);


--
-- Name: rwa_categories_name_bbbe843c_like; Type: INDEX; Schema: public; Owner: gli
--

CREATE INDEX rwa_categories_name_bbbe843c_like ON public.rwa_categories USING btree (name varchar_pattern_ops);


--
-- Name: rwa_categories_order_645aea7b; Type: INDEX; Schema: public; Owner: gli
--

CREATE INDEX rwa_categories_order_645aea7b ON public.rwa_categories USING btree ("order");


--
-- Name: shopping_categories_name_87272f6e_like; Type: INDEX; Schema: public; Owner: gli
--

CREATE INDEX shopping_categories_name_87272f6e_like ON public.shopping_categories USING btree (name varchar_pattern_ops);


--
-- Name: shopping_categories_order_38dadc9d; Type: INDEX; Schema: public; Owner: gli
--

CREATE INDEX shopping_categories_order_38dadc9d ON public.shopping_categories USING btree ("order");


--
-- Name: shopping_or_created_912a6b_idx; Type: INDEX; Schema: public; Owner: gli
--

CREATE INDEX shopping_or_created_912a6b_idx ON public.shopping_orders USING btree (created_at DESC);


--
-- Name: shopping_or_custome_66824e_idx; Type: INDEX; Schema: public; Owner: gli
--

CREATE INDEX shopping_or_custome_66824e_idx ON public.shopping_orders USING btree (customer_id, status);


--
-- Name: shopping_or_order_n_0ddc42_idx; Type: INDEX; Schema: public; Owner: gli
--

CREATE INDEX shopping_or_order_n_0ddc42_idx ON public.shopping_orders USING btree (order_number);


--
-- Name: shopping_order_items_order_id_36d4448b; Type: INDEX; Schema: public; Owner: gli
--

CREATE INDEX shopping_order_items_order_id_36d4448b ON public.shopping_order_items USING btree (order_id);


--
-- Name: shopping_order_items_product_id_79be391b; Type: INDEX; Schema: public; Owner: gli
--

CREATE INDEX shopping_order_items_product_id_79be391b ON public.shopping_order_items USING btree (product_id);


--
-- Name: shopping_orders_customer_id_39dae0fc; Type: INDEX; Schema: public; Owner: gli
--

CREATE INDEX shopping_orders_customer_id_39dae0fc ON public.shopping_orders USING btree (customer_id);


--
-- Name: shopping_orders_order_number_bf3d25d1_like; Type: INDEX; Schema: public; Owner: gli
--

CREATE INDEX shopping_orders_order_number_bf3d25d1_like ON public.shopping_orders USING btree (order_number varchar_pattern_ops);


--
-- Name: shopping_pr_categor_c946bf_idx; Type: INDEX; Schema: public; Owner: gli
--

CREATE INDEX shopping_pr_categor_c946bf_idx ON public.shopping_products USING btree (category_id, status);


--
-- Name: shopping_pr_is_feat_450291_idx; Type: INDEX; Schema: public; Owner: gli
--

CREATE INDEX shopping_pr_is_feat_450291_idx ON public.shopping_products USING btree (is_featured DESC, created_at DESC);


--
-- Name: shopping_pr_product_75ea01_idx; Type: INDEX; Schema: public; Owner: gli
--

CREATE INDEX shopping_pr_product_75ea01_idx ON public.shopping_products USING btree (product_type, status);


--
-- Name: shopping_products_category_id_1e3ef60c; Type: INDEX; Schema: public; Owner: gli
--

CREATE INDEX shopping_products_category_id_1e3ef60c ON public.shopping_products USING btree (category_id);


--
-- Name: solana_transactions_transaction_hash_045f83c1_like; Type: INDEX; Schema: public; Owner: gli
--

CREATE INDEX solana_transactions_transaction_hash_045f83c1_like ON public.solana_transactions USING btree (transaction_hash varchar_pattern_ops);


--
-- Name: solana_transactions_user_id_52233802; Type: INDEX; Schema: public; Owner: gli
--

CREATE INDEX solana_transactions_user_id_52233802 ON public.solana_transactions USING btree (user_id);


--
-- Name: solana_users_groups_group_id_b1c0d751; Type: INDEX; Schema: public; Owner: gli
--

CREATE INDEX solana_users_groups_group_id_b1c0d751 ON public.solana_users_groups USING btree (group_id);


--
-- Name: solana_users_groups_solanauser_id_11c89e39; Type: INDEX; Schema: public; Owner: gli
--

CREATE INDEX solana_users_groups_solanauser_id_11c89e39 ON public.solana_users_groups USING btree (solanauser_id);


--
-- Name: solana_users_user_permissions_permission_id_ba026ff1; Type: INDEX; Schema: public; Owner: gli
--

CREATE INDEX solana_users_user_permissions_permission_id_ba026ff1 ON public.solana_users_user_permissions USING btree (permission_id);


--
-- Name: solana_users_user_permissions_solanauser_id_d59b0da2; Type: INDEX; Schema: public; Owner: gli
--

CREATE INDEX solana_users_user_permissions_solanauser_id_d59b0da2 ON public.solana_users_user_permissions USING btree (solanauser_id);


--
-- Name: solana_users_username_02a6e338_like; Type: INDEX; Schema: public; Owner: gli
--

CREATE INDEX solana_users_username_02a6e338_like ON public.solana_users USING btree (username varchar_pattern_ops);


--
-- Name: solana_users_wallet_address_49950d1a_like; Type: INDEX; Schema: public; Owner: gli
--

CREATE INDEX solana_users_wallet_address_49950d1a_like ON public.solana_users USING btree (wallet_address varchar_pattern_ops);


--
-- Name: strategy_ph_order_bc8c62_idx; Type: INDEX; Schema: public; Owner: gli
--

CREATE INDEX strategy_ph_order_bc8c62_idx ON public.strategy_phases USING btree ("order", is_active);


--
-- Name: team_member_order_a5326a_idx; Type: INDEX; Schema: public; Owner: gli
--

CREATE INDEX team_member_order_a5326a_idx ON public.team_members USING btree ("order", is_active);


--
-- Name: token_ecosy_order_643813_idx; Type: INDEX; Schema: public; Owner: gli
--

CREATE INDEX token_ecosy_order_643813_idx ON public.token_ecosystems USING btree ("order", is_active);


--
-- Name: admin_users admin_users_grade_id_d7e8ab63_fk_admin_grades_id; Type: FK CONSTRAINT; Schema: public; Owner: gli
--

ALTER TABLE ONLY public.admin_users
    ADD CONSTRAINT admin_users_grade_id_d7e8ab63_fk_admin_grades_id FOREIGN KEY (grade_id) REFERENCES public.admin_grades(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: admin_users admin_users_user_id_5db507a7_fk_solana_users_id; Type: FK CONSTRAINT; Schema: public; Owner: gli
--

ALTER TABLE ONLY public.admin_users
    ADD CONSTRAINT admin_users_user_id_5db507a7_fk_solana_users_id FOREIGN KEY (user_id) REFERENCES public.solana_users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: gli
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: gli
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: gli
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: gli
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_solana_users_id; Type: FK CONSTRAINT; Schema: public; Owner: gli
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_solana_users_id FOREIGN KEY (user_id) REFERENCES public.solana_users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: face_verifications face_verifications_user_id_e72defbc_fk_solana_users_id; Type: FK CONSTRAINT; Schema: public; Owner: gli
--

ALTER TABLE ONLY public.face_verifications
    ADD CONSTRAINT face_verifications_user_id_e72defbc_fk_solana_users_id FOREIGN KEY (user_id) REFERENCES public.solana_users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: grade_permissions grade_permissions_grade_id_59c9bf2e_fk_admin_grades_id; Type: FK CONSTRAINT; Schema: public; Owner: gli
--

ALTER TABLE ONLY public.grade_permissions
    ADD CONSTRAINT grade_permissions_grade_id_59c9bf2e_fk_admin_grades_id FOREIGN KEY (grade_id) REFERENCES public.admin_grades(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: grade_permissions grade_permissions_permission_id_f2072039_fk_admin_per; Type: FK CONSTRAINT; Schema: public; Owner: gli
--

ALTER TABLE ONLY public.grade_permissions
    ADD CONSTRAINT grade_permissions_permission_id_f2072039_fk_admin_per FOREIGN KEY (permission_id) REFERENCES public.admin_permissions(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: investments investments_investor_id_96559232_fk_solana_users_id; Type: FK CONSTRAINT; Schema: public; Owner: gli
--

ALTER TABLE ONLY public.investments
    ADD CONSTRAINT investments_investor_id_96559232_fk_solana_users_id FOREIGN KEY (investor_id) REFERENCES public.solana_users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: investments investments_rwa_asset_id_09fe90d8_fk_rwa_assets_id; Type: FK CONSTRAINT; Schema: public; Owner: gli
--

ALTER TABLE ONLY public.investments
    ADD CONSTRAINT investments_rwa_asset_id_09fe90d8_fk_rwa_assets_id FOREIGN KEY (rwa_asset_id) REFERENCES public.rwa_assets(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: rwa_assets rwa_assets_category_id_61d8811d_fk_rwa_categories_id; Type: FK CONSTRAINT; Schema: public; Owner: gli
--

ALTER TABLE ONLY public.rwa_assets
    ADD CONSTRAINT rwa_assets_category_id_61d8811d_fk_rwa_categories_id FOREIGN KEY (category_id) REFERENCES public.rwa_categories(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: shopping_order_items shopping_order_items_order_id_36d4448b_fk_shopping_orders_id; Type: FK CONSTRAINT; Schema: public; Owner: gli
--

ALTER TABLE ONLY public.shopping_order_items
    ADD CONSTRAINT shopping_order_items_order_id_36d4448b_fk_shopping_orders_id FOREIGN KEY (order_id) REFERENCES public.shopping_orders(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: shopping_order_items shopping_order_items_product_id_79be391b_fk_shopping_; Type: FK CONSTRAINT; Schema: public; Owner: gli
--

ALTER TABLE ONLY public.shopping_order_items
    ADD CONSTRAINT shopping_order_items_product_id_79be391b_fk_shopping_ FOREIGN KEY (product_id) REFERENCES public.shopping_products(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: shopping_orders shopping_orders_customer_id_39dae0fc_fk_solana_users_id; Type: FK CONSTRAINT; Schema: public; Owner: gli
--

ALTER TABLE ONLY public.shopping_orders
    ADD CONSTRAINT shopping_orders_customer_id_39dae0fc_fk_solana_users_id FOREIGN KEY (customer_id) REFERENCES public.solana_users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: shopping_products shopping_products_category_id_1e3ef60c_fk_shopping_; Type: FK CONSTRAINT; Schema: public; Owner: gli
--

ALTER TABLE ONLY public.shopping_products
    ADD CONSTRAINT shopping_products_category_id_1e3ef60c_fk_shopping_ FOREIGN KEY (category_id) REFERENCES public.shopping_categories(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: solana_transactions solana_transactions_user_id_52233802_fk_solana_users_id; Type: FK CONSTRAINT; Schema: public; Owner: gli
--

ALTER TABLE ONLY public.solana_transactions
    ADD CONSTRAINT solana_transactions_user_id_52233802_fk_solana_users_id FOREIGN KEY (user_id) REFERENCES public.solana_users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: solana_users_groups solana_users_groups_group_id_b1c0d751_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: gli
--

ALTER TABLE ONLY public.solana_users_groups
    ADD CONSTRAINT solana_users_groups_group_id_b1c0d751_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: solana_users_groups solana_users_groups_solanauser_id_11c89e39_fk_solana_users_id; Type: FK CONSTRAINT; Schema: public; Owner: gli
--

ALTER TABLE ONLY public.solana_users_groups
    ADD CONSTRAINT solana_users_groups_solanauser_id_11c89e39_fk_solana_users_id FOREIGN KEY (solanauser_id) REFERENCES public.solana_users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: solana_users_user_permissions solana_users_user_pe_permission_id_ba026ff1_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: gli
--

ALTER TABLE ONLY public.solana_users_user_permissions
    ADD CONSTRAINT solana_users_user_pe_permission_id_ba026ff1_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: solana_users_user_permissions solana_users_user_pe_solanauser_id_d59b0da2_fk_solana_us; Type: FK CONSTRAINT; Schema: public; Owner: gli
--

ALTER TABLE ONLY public.solana_users_user_permissions
    ADD CONSTRAINT solana_users_user_pe_solanauser_id_d59b0da2_fk_solana_us FOREIGN KEY (solanauser_id) REFERENCES public.solana_users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

